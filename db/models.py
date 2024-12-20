from sqlalchemy import (
    Column,
    SmallInteger,
    Integer,
    BigInteger,
    String,
    TIMESTAMP,
    ForeignKey,
    Boolean,
    Index, Float, Enum, LargeBinary, UniqueConstraint, func, select,
)
from sqlalchemy.dialects.postgresql import JSONB
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from db import get_async_session

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

Base = declarative_base()


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    telegram_id = Column(BigInteger, nullable=False, unique=True)

    tags = relationship("Tag", back_populates="user", lazy="select")
    files = relationship("File", back_populates="user", lazy="select")


class Template(Base):
    __tablename__ = "template"
    id = Column(Integer, primary_key=True)
    filename = Column(String, nullable=False)
    message_id = Column(Integer, nullable=False)
    vars = Column(JSONB, nullable=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    tag_id = Column(Integer, ForeignKey("tag.id"), nullable=True)

    user = relationship("User", back_populates="files", lazy="select")
    tag = relationship("Tag", back_populates="files", lazy="select")
    files = relationship("File", back_populates="template", lazy="select")

    __table_args__ = (
        UniqueConstraint('filename', 'user_id', name='uix_template_user'),
    )

    @staticmethod
    async def generate_unique_filename(session: AsyncSession, base_filename: str, user_id: int) -> str:
        if '.' in base_filename:
            base_name, extension = base_filename.rsplit('.', 1)
        else:
            base_name, extension = base_filename, ''  # Если расширения нет, просто берем весь filename как base_name
        # Запрос на подсчет файлов с таким же именем у конкретного пользователя
        query = select(func.count()).where(Template.filename == base_filename, Template.user_id == user_id)
        result = await session.execute(
            query
        )
        count = result.scalar()

        # Если файл с таким именем существует, добавляем суффикс с числом
        if count > 0:
            counter = 1
            while True:
                # Если расширение есть, добавляем суффикс, иначе просто добавляем число
                if extension:
                    new_filename = f"{base_name}_{counter}.{extension}"
                else:
                    new_filename = f"{base_name}_{counter}"

                query = select(func.count()).where(Template.filename == new_filename, Template.user_id == user_id)
                result = await session.execute(
                    query
                )
                count = result.scalar()
                if count == 0:  # Если имя уникально, возвращаем его
                    return new_filename
                counter += 1
        return base_filename  # Если имя уникально, возвращаем исходное имя


class File(Base):
    __tablename__ = "file"

    id = Column(Integer, primary_key=True)
    filename = Column(String, nullable=False)
    vars = Column(JSONB, nullable=False)
    template_id = Column(Integer, ForeignKey("template.id"), nullable=False)

    template = relationship("Template", back_populates="files", lazy="select")


class Tag(Base):
    __tablename__ = "tag"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)

    user = relationship("User", back_populates="tags", lazy="select")
    templates = relationship("Template", back_populates="tag", lazy="select")
    files = relationship("File", back_populates="tag", lazy="select")

    __table_args__ = (
        UniqueConstraint('name', 'user_id', name='uix_name_user'),
    )