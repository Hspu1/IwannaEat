from uuid import UUID

from fastapi import APIRouter, status

from src.core.dependencies import PgRoSession, StripeClientDep

from ..handlers.pay_link import pay_link

generate_link_router = APIRouter(prefix="/billing")


@generate_link_router.post(
    "/test-pay-link/{top_up_id}", status_code=status.HTTP_201_CREATED
)
async def generate_link(
    session: PgRoSession,
    stripe_client: StripeClientDep,
    top_up_id: UUID,
) -> str:

    return await pay_link(
        session=session, stripe_client=stripe_client, top_up_id=top_up_id
    )
