from io import BytesIO
from typing import List, Text

from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile
from fastapi_pagination import Params
from sqlalchemy import or_
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_jwt_auth import AuthJWT
from fastapi_pagination.ext.sqlalchemy import paginate

from db import get_async_session
from db.models import File
from schemes.file import FilesResponse, FileResponse, FileCreate
from services.file import get_files, create_file
from services.tag import get_user_tags

router = APIRouter(prefix="/files", tags=["File"])

@router.get("", response_model=FilesResponse)
async def get_users_files(
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

    conditions = [(File.user_id == user_id)]

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
        conditions.append(File.tag_id.in_(tag_ids))

    if search is not None:
        search = search.strip()
        conditions.append(File.filename.ilike(f"%{search}%"))

    query_files = await get_files(conditions)
    files = await paginate(session, query_files, params=params)

    return {
        "status": "success",
        "data":files,
        "details": {"msg": "Files found."}
    }


@router.post("/upload", response_model=FileResponse)
async def upload_file(
        # file: UploadFile,
        # msg_id: int,
        data: FileCreate,
        session: AsyncSession = Depends(get_async_session),
        authorize: AuthJWT = Depends(),
):
    authorize.jwt_required()
    user_id = authorize.get_jwt_subject()
    # content = await file.read()
    # fileio = BytesIO(content)
    file = await create_file(data, session)

    return {
        "status": "success",
        "data": file,
        "details": {"msg": "File uploaded."}
    }