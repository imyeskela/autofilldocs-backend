from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_jwt_auth import AuthJWT

from schemes.auth import JWTResponse, UserSignUp, UserLogin
from db import get_async_session
from services.auth import return_jwt
from services.user import check_existence, create_new_user, get_user_by_telegram_id

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("", response_model=JWTResponse)
async def signup(
        user_data: UserSignUp,
        session: AsyncSession = Depends(get_async_session),
        authorize: AuthJWT = Depends(),
):
    await check_existence(user_data.telegram_id, session)
    user = await create_new_user(user_data, session)

    return return_jwt(user, authorize)


@router.post("/login", response_model=JWTResponse)
async def login(
        user_data: UserLogin,
        session: AsyncSession = Depends(get_async_session),
        authorize: AuthJWT = Depends(),
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

    return return_jwt(user, authorize)
