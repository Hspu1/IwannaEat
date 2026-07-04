from uuid import UUID

from sqlalchemy import update
from sqlalchemy.exc import DBAPIError
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.exceptions import WalletBalanceOverflowError, WalletNotFoundError
from src.shared.postgres.models.schema import WalletsModel


async def top_up_balance(session: AsyncSession, user_id: UUID, amount: int) -> int:
    try:
        result = await session.execute(
            update(WalletsModel)
            .where(WalletsModel.user_id == user_id)
            .values(balance=WalletsModel.balance + amount)
            .returning(WalletsModel.balance)
        )

        new_balance = result.scalar_one_or_none()
        if new_balance is None:
            raise WalletNotFoundError(user_id=user_id)

        return int(new_balance)

    except DBAPIError as e:
        raise WalletBalanceOverflowError(user_id=user_id) from e
