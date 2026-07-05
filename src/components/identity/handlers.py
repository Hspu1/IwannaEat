from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from .repository import create_user_with_wallet


async def register_new_user(session: AsyncSession) -> str:
    user_id: UUID = await create_user_with_wallet(session=session)
    return str(user_id)
