from enum import StrEnum
from uuid import UUID

from fastapi import APIRouter, Response, status
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from iwe.core.dependencies import pg_session
from iwe.shared.postgres.enums import OrderStatus
from iwe.shared.postgres.schema import OrdersModel

#######################################################################################
#######################################################################################


class ResultMessages(StrEnum):
    USER_NOT_FOUND = "user not found"
    UNSUPPORTED_RESULT = "ya forgot to handle smth"


class ErrCauseState(StrEnum):
    OP_VIOLATES_FK_CONSTRAINT = "23503"


class ErrCauseConstraint(StrEnum):
    ORDERS_USER_ID_FK = "orders_user_id_fkey"


#######################################################################################
#######################################################################################

router = APIRouter()


@router.post("/initialize")
async def initialize_order(user_id: UUID, response: Response) -> UUID | ResultMessages:
    async with pg_session() as session:
        verdict = await get_order_id(session=session, user_id=user_id)

    match verdict:
        case UUID() as order_id:
            response.status_code = status.HTTP_201_CREATED
            return order_id

        case ResultMessages.USER_NOT_FOUND:
            response.status_code = status.HTTP_404_NOT_FOUND
            return verdict

        case _:
            response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            return ResultMessages.UNSUPPORTED_RESULT  # for debugging


#######################################################################################
#######################################################################################


async def get_order_id(session: AsyncSession, user_id: UUID) -> UUID | ResultMessages:
    raw_order_id = (
        pg_insert(OrdersModel)
        .values(user_id=user_id, status=OrderStatus.CREATED)
        .returning(OrdersModel.id)
    )
    try:
        order_id = await session.execute(raw_order_id)
        return order_id.scalar_one()

    except IntegrityError as err:
        driver_err = err.__cause__.__cause__  # wtf

        match (driver_err.sqlstate, driver_err.constraint_name):
            case (
                ErrCauseState.OP_VIOLATES_FK_CONSTRAINT,
                ErrCauseConstraint.ORDERS_USER_ID_FK,
            ):
                return ResultMessages.USER_NOT_FOUND

            case _:
                print(
                    f"IntegrityError unexpected shi in get_order_id: {
                        driver_err.sqlstate, driver_err.constraint_name
                    }"
                )
                raise err
