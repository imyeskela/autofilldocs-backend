from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession

from schemes.auth import JWTResponse, UserSignUp
from db import get_async_session
from services.user import check_existence, create_new_user

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("", response_model=JWTResponse)
async def signup(
        user_data: UserSignUp,
        session: AsyncSession = Depends(get_async_session)
):
    if not user_data.username:
        user_data.username = str(user_data.telegram_id)
    await check_existence(user_data.username, user_data.telegram_id, session)

    user = await create_new_user(user_data, session)

    return {
        "status": "success",
        "data": {
            "id": user.id,
            "token": "1123"
        },
        "details": None
    }
