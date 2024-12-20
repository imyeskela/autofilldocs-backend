from io import BytesIO
from typing import List, Text

from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile
from fastapi_pagination import Params
from sqlalchemy import or_
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_jwt_auth import AuthJWT
from fastapi_pagination.ext.sqlalchemy import paginate

from db import get_async_session
from db.models import Template
from schemes.template import TemplatesResponse, TemplateResponse, TemplateCreate
from services.template import get_templates, create_template, parse_template
from services.tag import get_user_tags, get_user_default_tag

router = APIRouter(prefix="/templates", tags=["Template"])


@router.get("", response_model=TemplatesResponse)
async def get_users_templates(
        tag_ids: List[int] = Query(None),
        search: str | None = None,
        params: Params = Depends(),
        session: AsyncSession = Depends(get_async_session),
        authorize: AuthJWT = Depends(),
):
    authorize.jwt_required()
    user_id = authorize.get_jwt_subject()

    user_tags = await get_user_tags(user_id, session)
    user_tag_ids = [tag.id for tag in user_tags if tag.id in tag_ids]

    conditions = [(Template.user_id == user_id)]

    if tag_ids is not None:
        # if tag_ids not in user_tag_ids:
        #     raise HTTPException(
        #         status_code=400,
        #         detail={
        #             "status": "failed",
        #             "data": None,
        #             "details": {"msg": "User does not have these tags."},
        #         }
        #     )
        conditions.append(Template.tag_id.in_(tag_ids))

    if search is not None:
        search = search.strip()
        conditions.append(Template.filename.ilike(f"%{search}%"))

    query_files = await get_templates(conditions)
    files = await paginate(session, query_files, params=params)

    return {
        "status": "success",
        "data":files,
        "details": {"msg": "Files found."}
    }


@router.post("/upload", response_model=TemplateResponse)
async def upload_template(
        file: UploadFile,
        msg_id: int,
        session: AsyncSession = Depends(get_async_session),
        authorize: AuthJWT = Depends(),
):
    authorize.jwt_required()
    user_id = authorize.get_jwt_subject()
    content = await file.read()
    fileio = BytesIO(content)
    parsed_data = await parse_template(fileio)
    default_tag = await get_user_default_tag(user_id, session)
    data = TemplateCreate(**parsed_data, message_id=msg_id, user_id=user_id, tag_id=default_tag.id)
    file = await create_template(data, session)

    return {
        "status": "success",
        "data": file,
        "details": {"msg": "File uploaded."}
    }