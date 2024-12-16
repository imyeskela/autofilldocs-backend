from sqlalchemy import (
    Column,
    SmallInteger,
    Integer,
    BigInteger,
    String,
    TIMESTAMP,
    ForeignKey,
    Boolean,
    Index, Float, Enum, LargeBinary,
)
from sqlalchemy.dialects.postgresql import JSONB
from passlib.context import CryptContext

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

Base = declarative_base()


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    telegram_id = Column(BigInteger, nullable=False, unique=True)
    username = Column(String, nullable=False, unique=True)

    tags = relationship("Tag", back_populates="user", lazy="select")
    files = relationship("File", back_populates="user", lazy="select")


class File(Base):
    __tablename__ = "file"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    message_id = Column(Integer, nullable=False)
    vars = Column(JSONB, nullable=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    tag_id = Column(Integer, ForeignKey("tag.id"), nullable=True)

    user = relationship("User", back_populates="files", lazy="select")
    tag = relationship("Tag", back_populates="files", lazy="select")


class Tag(Base):
    __tablename__ = "tag"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)

    user = relationship("User", back_populates="tags", lazy="select")
    files = relationship("File", back_populates="tag", lazy="select")