from pydantic import BaseModel


class JWT(BaseModel):
    id: int
    token: str


class JWTResponse(BaseModel):
    status: str
    data: JWT
    details: dict | None


class UserSignUp(BaseModel):
    telegram_id: int
    username: str | None = None