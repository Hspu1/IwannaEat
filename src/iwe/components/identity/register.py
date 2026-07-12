from uuid import UUID

from fastapi import APIRouter, status
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.ext.asyncio import AsyncSession

from iwe.core.dependencies import pg_session
from iwe.shared.postgres.schema import UsersModel, WalletsModel

router = APIRouter()


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register() -> dict[str, str]:
    async with pg_session() as session:
        user_id: UUID = await create_user_with_wallet(session=session)

    return {
        "user_id": str(user_id),
    }


#######################################################################################
#######################################################################################


async def create_user_with_wallet(session: AsyncSession) -> UUID:
    user_result = await session.execute(
        pg_insert(UsersModel).returning(UsersModel.id),
    )
    user_id = user_result.scalar_one()

    await session.execute(pg_insert(WalletsModel).values(user_id=user_id))
    return user_id
