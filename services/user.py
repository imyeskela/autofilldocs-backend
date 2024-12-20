from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from fastapi import HTTPException
from db.models import User
from schemes.auth import UserSignUp
from schemes.tag import TagCreate
from services.tag import create_tag


async def get_user_by_telegram_id(telegram_id: int, session: AsyncSession) -> User:
    query = select(User).where(User.telegram_id == telegram_id)
    result = await session.execute(query)
    user = result.scalar_one_or_none()
    return user

async def check_existence(telegram_id: int, session: AsyncSession):
    """Сhecks if the user is in the database"""
    user = await get_user_by_telegram_id(telegram_id, session)
    if user:
        raise HTTPException(
            status_code=400,
            detail={
                "status": "failed",
                "data": None,
                "details": {"msg": "User exists."},
            }
        )

async def create_new_user(user_data: UserSignUp, session: AsyncSession) -> User:
    """Func for creations new user"""
    user = User(**user_data.model_dump())
    session.add(user)
    await session.commit()
    await session.refresh(user)
    await create_tag(TagCreate(name="Общая", user_id=user.id), session)
    return user


