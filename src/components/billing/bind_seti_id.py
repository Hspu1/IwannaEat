from uuid import UUID

from fastapi import APIRouter, Response, status
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.dependencies import PgSession
from src.shared.postgres.schema import UserCardsModel

router = APIRouter(prefix="/bind")


#######################################################################################
#######################################################################################


class BindRequest(BaseModel):
    user_id: UUID
    seti_id: str = Field(
        description="Stripe SetupIntent ID",
        pattern=r"^seti_[a-zA-Z0-9]{24}$",
    )


#######################################################################################
#######################################################################################


@router.post("/seti-id")
async def bind_setup_intent(
    session: PgSession, request: BindRequest, response: Response
) -> str | None:

    verdict = await bind_seti_id(
        session=session, user_id=request.user_id, seti_id=request.seti_id
    )

    if isinstance(verdict, str):
        response.status_code = status.HTTP_404_NOT_FOUND
        return verdict

    if not verdict:
        response.status_code = status.HTTP_409_CONFLICT
        return "ts already bound"

    response.status_code = status.HTTP_201_CREATED
    return None


#######################################################################################
#######################################################################################


async def bind_seti_id(session: AsyncSession, user_id: UUID, seti_id: str) -> str | bool:
    stmt = (
        pg_insert(UserCardsModel)
        .values(user_id=user_id, seti_id=seti_id)
        .on_conflict_do_nothing()
    )
    try:
        res = await session.execute(stmt)

    except IntegrityError as err:
        if "violates foreign key constraint" in str(err.orig):
            return "user not found"
        raise err

    else:
        return res.rowcount > 0
