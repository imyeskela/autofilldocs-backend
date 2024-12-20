from sqlalchemy import select
from typing import Sequence

from schemes.tag import TagCreate
from db.models import Tag
from sqlalchemy.ext.asyncio import AsyncSession

async def create_tag(tag_data: TagCreate, session: AsyncSession) -> Tag:
    new_tag = Tag(**tag_data.model_dump(exclude_unset=True))
    session.add(new_tag)
    await session.commit()
    await session.refresh(new_tag)
    return new_tag


async def get_user_tags(user_id: int, session: AsyncSession) ->  Sequence[Tag]:
    query = select(Tag).where(Tag.user_id == user_id).order_by(Tag.id.desc())
    result = await session.execute(query)
    tags = result.scalars().all()
    return tags