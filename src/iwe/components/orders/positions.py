from enum import StrEnum
from uuid import UUID

from fastapi import APIRouter, Response, status
from pydantic import BaseModel, Field
from sqlalchemy import literal, select
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.ext.asyncio import AsyncSession

from iwe.core.dependencies import pg_session
from iwe.shared.postgres.schema import DishesModel, OrderContentsModel

#######################################################################################
#######################################################################################


class PositionsRequest(BaseModel):
    dish_name: str = Field(min_length=6, max_length=67, pattern=r"(?i)burger")
    qty: int = Field(ge=0, le=100)


#######################################################################################
#######################################################################################


class ResultMessages(StrEnum):
    SUCCESS = "success"
    INVALID_ORDER_OR_DISH = "order or dish not found"
    UNSUPPORTED_RESULT = "ya forgot to handle smth"


#######################################################################################
#######################################################################################

router = APIRouter()


@router.post("/{order_id}/positions")
async def manage_position(
    order_id: UUID, request: PositionsRequest, response: Response
) -> dict[str, ResultMessages]:

    async with pg_session() as session:
        verdict = await add_position(
            session=session,
            order_id=order_id,
            dish_name=request.dish_name,
            qty=request.qty,
        )

    match verdict:
        case ResultMessages.SUCCESS:
            response.status_code = status.HTTP_201_CREATED
            return {
                "verdict": verdict,
            }

        case ResultMessages.INVALID_ORDER_OR_DISH:
            response.status_code = status.HTTP_404_NOT_FOUND
            return {
                "verdict": verdict,
            }

        case _:
            response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            return {
                "huh": ResultMessages.UNSUPPORTED_RESULT,
            }  # for debugging


#######################################################################################
#######################################################################################


async def add_position(
    session: AsyncSession, order_id: UUID, dish_name: str, qty: int
) -> ResultMessages:

    stmt = (
        pg_insert(OrderContentsModel)
        .from_select(
            ["order_id", "dish_id", "price_cents", "qty"],
            select(
                literal(order_id),
                DishesModel.id,
                DishesModel.info["price_cents"].as_integer(),
                literal(qty),
            ).where(
                DishesModel.info["name"].as_string() == dish_name,
                DishesModel.is_available.is_(True),
            ),
        )
        .on_conflict_do_update(
            index_elements=["order_id", "dish_id"],  # composite PK
            set_={"qty": qty},
        )
        .returning(OrderContentsModel.dish_id)
    )

    res = await session.execute(stmt)
    if not res.scalar_one_or_none():
        return ResultMessages.INVALID_ORDER_OR_DISH

    return ResultMessages.SUCCESS
