from io import BytesIO
from typing import List, Sequence

from fastapi import Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_

from db.models import File
from schemes.file import FileCreate


async def get_files(conditions: List) -> Query:
    query = select(File).where(and_(*conditions)).order_by(File.message_id.desc())
    return query

async def parse_file(file: BytesIO, session: AsyncSession):
    pass

async def create_file(file_data: FileCreate, session: AsyncSession) -> File:
    new_file = File(**file_data.model_dump())
    session.add(new_file)
    await session.commit()
    await session.refresh(new_file)
    return new_file

