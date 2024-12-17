from pydantic import BaseModel

class FileResponse(BaseModel):
    id: int
    name: str
    message_id: int
    vars: dict
    user_id: int
    tag_id: int