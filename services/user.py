from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
from sqlalchemy.orm import selectinload
from fastapi import HTTPException

from db.models import User
from schemes.auth import UserSignUp
from schemes.tag import TagCreate
from services.tag import create_new_tag


async def check_existence(username, telegram_id, session: AsyncSession):
    """Сhecks if the user is in the database"""
    filter_args = [
        (User.username == username),
        (User.telegram_id == telegram_id),
    ]

    query = select(User).options(
            selectinload(User.files),
            selectinload(User.tags),
        ).where(or_(*filter_args))
    result = await session.execute(query)
    user = result.first()
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
    await create_new_tag(TagCreate(name="Общая", user_id=user.id), session)
    return user