from fastapi_jwt_auth import AuthJWT
from starlette.responses import JSONResponse

from db.models import User


def return_jwt(user: User, authorize: AuthJWT, refresh_token: str | None = None):
    user_data = {
        "user_id": user.id,
        "telegram_id": user.telegram_id,
    }

    access_token = authorize.create_access_token(
        subject=user.id, user_claims=user_data
    )
    if not refresh_token:
        refresh_token = authorize.create_refresh_token(
            subject=user.id, user_claims=user_data
        )

    return JSONResponse(
        status_code=200,
        content={
            "status": "success",
            "data": {
                "id": user.id,
                "token": access_token,
                "refresh": refresh_token
            },
            "details": {"msg": "User successfully authorized."}
        }
    )