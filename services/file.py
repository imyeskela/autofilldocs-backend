from io import BytesIO
from typing import List, Sequence
from docxtpl import DocxTemplate
from fastapi import Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_

from db.models import File
from schemes.file import FileCreate


async def get_files(conditions: List) -> Query:
    query = select(File).where(and_(*conditions)).order_by(File.message_id.desc())
    return query


async def parse_file(file: BytesIO) -> dict:
    try:
        docx_file = DocxTemplate(file)
        vars_set = docx_file.get_undeclared_template_variables()
        if not vars_set:
            raise HTTPException(status_code=400, detail="No variables found in the document")
        filename =  "Untitled"
        variables = {var: "" for var in docx_file.get_undeclared_template_variables()}

        if not variables:
            raise HTTPException(status_code=400, detail="No variables found in the document")

        return {
            "filename": filename,
            "vars": variables
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error parsing template: {str(e)}")


async def create_file(file_data: FileCreate, session: AsyncSession) -> File:
    unique_filename = await File.generate_unique_filename(session, file_data.filename, file_data.user_id)
    print(unique_filename)
    file_data.filename=unique_filename
    new_file = File(**file_data.model_dump())
    session.add(new_file)
    await session.commit()
    await session.refresh(new_file)
    return new_file