from schemes.tag import TagCreate
from db.models import Tag
from sqlalchemy.ext.asyncio import AsyncSession

async def create_new_tag(tag_data: TagCreate, session: AsyncSession) -> Tag:
    new_tag = Tag(**tag_data.model_dump(exclude_unset=True))
    session.add(new_tag)
    await session.commit()
    await session.refresh(new_tag)
    return new_tag