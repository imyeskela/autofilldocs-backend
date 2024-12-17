from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession

from schemes.auth import JWTResponse, UserSignUp, UserLogin
from db import get_async_session
from services.user import check_existence, create_new_user, get_user_by_telegram_id

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("", response_model=JWTResponse)
async def signup(
        user_data: UserSignUp,
        session: AsyncSession = Depends(get_async_session)
):
    await check_existence(user_data.telegram_id, session)
    user = await create_new_user(user_data, session)
    return {
        "status": "success",
        "data": {
            "id": user.id,
            "token": "1123"
        },
        "details": None
    }

@router.post("/login", response_model=JWTResponse)
async def login(
        user_data: UserLogin,
        session: AsyncSession = Depends(get_async_session)
):

    user = await get_user_by_telegram_id(user_data.telegram_id, session)
    if user is None:
        raise HTTPException(
            status_code=404,
            detail={
                "status": "failed",
                "data": None,
                "details": {"msg": "User not found."},
            },
        )

    return {
        "status": "success",
        "data": {
            "id": user.id,
            "token": "1123"
        },
        "details": None
    }
