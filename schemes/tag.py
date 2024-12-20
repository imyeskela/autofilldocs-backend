from typing import List

from pydantic import BaseModel

from schemes.template import TemplateResponse


class TagCreate(BaseModel):
    name: str
    user_id: int
    files: List[TemplateResponse] | None = None