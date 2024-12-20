from pydantic import BaseModel
from typing import List
from fastapi_pagination import Page

class FileReturn(BaseModel):
    id: int
    filename: str
    tag_id: int


class FileRead(BaseModel):
    id: int
    filename: str
    message_id: int
    vars: dict
    tag_id: int


class FileResponse(BaseModel):
    status: str
    data: FileRead
    details: dict


class FilesResponse(BaseModel):
    status: str
    data: Page[FileReturn]
    details: dict


class FilesQuery(BaseModel):
    tag_ids: List[int]
    search: str


class FileCreate(BaseModel):
    filename: str
    message_id: int
    vars: dict
    tag_id: int
    user_id: int