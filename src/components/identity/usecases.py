from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.exceptions import WhyFuckingRaceConditionError
from src.shared.postgres.models.schema import UsersModel, WalletsModel


async def register_new_user(session: AsyncSession) -> str:
    try:
        user_result = await session.execute(insert(UsersModel).returning(UsersModel.id))
        user_id = user_result.scalar_one()
        await session.execute(insert(WalletsModel).values(user_id=user_id))

        return str(user_id)

    except IntegrityError as e:
        raise WhyFuckingRaceConditionError from e
