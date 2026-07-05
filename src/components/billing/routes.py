from uuid import UUID

from fastapi import APIRouter, status
from pydantic import BaseModel, Field

from src.core.dependencies import PgSession

from .handlers import top_up_balance

billing_router = APIRouter(prefix="/billing")


class TopUpRequest(BaseModel):
    user_id: UUID
    amount: int = Field(gt=0, description="Amount in minor units (789.99 --> 78999)")


@billing_router.post("/top-up", status_code=status.HTTP_200_OK)
async def top_up(session: PgSession, request: TopUpRequest) -> int:
    return await top_up_balance(
        session=session, user_id=request.user_id, amount=request.amount
    )
