from uuid import UUID

from fastapi import APIRouter, status
from pydantic import BaseModel, Field

from src.core.dependencies import PgSession

from ..handlers.top_up_request import top_up_request

create_request_router = APIRouter(prefix="/billing")


class TopUpRequest(BaseModel):
    user_id: UUID
    amount: int = Field(ge=5000, description="Amount in minor units (789.99 --> 78999)")


@create_request_router.post("/top-up", status_code=status.HTTP_200_OK)
async def create_request(session: PgSession, request: TopUpRequest) -> str:
    return await top_up_request(
        session=session, user_id=request.user_id, amount=request.amount
    )
