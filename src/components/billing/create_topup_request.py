from uuid import UUID

from fastapi import APIRouter, Response, status
from pydantic import BaseModel, Field
from sqlalchemy import func, select
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.dependencies import PgSession
from src.shared.postgres.enums import OutboxEventType, TopUpStatus
from src.shared.postgres.schema import (
    OutboxEventsModel,
    UserCardsModel,
    WalletTopUpsModel,
)

router = APIRouter()


#######################################################################################
#######################################################################################


class TopUpRequest(BaseModel):
    """should be order_id instead of amount acshually"""

    user_id: UUID
    amount: int = Field(
        ge=5000,
        description="Amount in minor units (789.99 --> 78999)",
    )
    idempotency_key: UUID


#######################################################################################
#######################################################################################


@router.post("/top-up")
async def create_request(
    session: PgSession, request: TopUpRequest, response: Response
) -> str | None:

    verdict = await create_topup_request(
        session=session,
        user_id=request.user_id,
        amount=request.amount,
        idempotency_key=request.idempotency_key,
    )

    if isinstance(verdict, str):
        response.status_code = (
            status.HTTP_202_ACCEPTED
            if verdict == "hold the fuck up"
            else status.HTTP_404_NOT_FOUND
        )
        return verdict

    if not verdict:
        response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        return "no card lad"

    response.status_code = status.HTTP_201_CREATED
    return None


#######################################################################################
#######################################################################################


async def create_topup_request(
    session: AsyncSession, user_id: UUID, amount: int, idempotency_key: UUID
) -> str | bool:

    stmt_top_up = (
        pg_insert(WalletTopUpsModel)
        .values(
            user_id=user_id,
            idempotency_key=idempotency_key,
            amount=amount,
            status=TopUpStatus.PENDING,
        )
        .on_conflict_do_nothing()
    )

    try:
        res_top_up = await session.execute(stmt_top_up)

    except IntegrityError as err:
        if "violates foreign key constraint" in str(err.orig):
            return "user not found"
        raise err

    else:
        if not res_top_up.rowcount:
            card_res = await session.execute(
                select(1).where(UserCardsModel.user_id == user_id).limit(1)
            )
            if card_res.one_or_none() is None:
                return False

            return "hold the fuck up"

    event_type = OutboxEventType.HOLD_FUNDS_REQUESTED
    payload = func.json_build_object(
        "user_id",
        user_id,
        "amount",
        amount,
        "seti_id",
        UserCardsModel.seti_id,
        "idempotency_key",
        idempotency_key,
    )

    stmt_outbox = (
        pg_insert(OutboxEventsModel)
        .from_select(
            ["event_type", "payload"],
            select(event_type, payload)
            .select_from(UserCardsModel)
            .where(UserCardsModel.user_id == user_id),
        )
        .on_conflict_do_nothing()
    )

    res_outbox = await session.execute(stmt_outbox)
    return res_outbox.rowcount > 0
