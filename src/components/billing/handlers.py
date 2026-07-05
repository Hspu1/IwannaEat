from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from .repository import update_balance


async def top_up_balance(session: AsyncSession, user_id: UUID, amount: int) -> int:
    new_balance: int = await update_balance(
        session=session, user_id=user_id, amount=amount
    )
    return new_balance
