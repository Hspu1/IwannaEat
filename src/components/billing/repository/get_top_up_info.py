from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.shared.postgres.schema import WalletTopUpsModel


async def get_top_up_info(session: AsyncSession, top_up_id: UUID) -> tuple[int, UUID]:
    stmt = select(WalletTopUpsModel.amount, WalletTopUpsModel.user_id).where(
        WalletTopUpsModel.id == top_up_id
    )
    result = await session.execute(stmt)
    return result.one()
