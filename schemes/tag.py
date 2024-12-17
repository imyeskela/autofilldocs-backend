from typing import List

from pydantic import BaseModel

from schemes.file import FileResponse


class TagCreate(BaseModel):
    name: str
    user_id: int
    files: List[FileResponse] | None = None