from pydantic import BaseModel
from typing import List
from fastapi_pagination import Page

class TemplateReturn(BaseModel):
    id: int
    filename: str
    tag_id: int


class TemplateRead(BaseModel):
    id: int
    filename: str
    message_id: int
    vars: dict
    tag_id: int


class TemplateResponse(BaseModel):
    status: str
    data: TemplateRead
    details: dict


class TemplatesResponse(BaseModel):
    status: str
    data: Page[TemplateReturn]
    details: dict


class TemplateCreate(BaseModel):
    filename: str
    message_id: int
    vars: dict
    tag_id: int
    user_id: int