from uuid import UUID

from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.exceptions import WhyFuckingRaceConditionError
from src.shared.postgres.schema import UsersModel, WalletsModel


async def create_user_with_wallet(session: AsyncSession) -> UUID:
    try:
        user_result = await session.execute(insert(UsersModel).returning(UsersModel.id))
        user_id = user_result.scalar_one()
        await session.execute(insert(WalletsModel).values(user_id=user_id))

        return user_id

    except IntegrityError as e:
        raise WhyFuckingRaceConditionError from e
