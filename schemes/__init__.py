from pydantic import BaseModel

from tools.config import config_read

config = config_read("config.ini")

class Settings(BaseModel):
    authjwt_secret_key: str = config.get("JWT", "secret")
    authjwt_access_token_expires: int = int(config.get("JWT", "token_expires_sec"))
    authjwt_algorithm: str = "HS256"
    authjwt_refresh_token_expires: int = int(config.get("JWT", "refresh_token_expires_sec"))