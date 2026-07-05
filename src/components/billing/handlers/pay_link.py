from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from stripe import StripeClient, error

from src.core.env_conf import stripe_stg

from ..repository.generate_pay_link import generate_pay_link
from ..repository.get_top_up_info import get_top_up_info


async def pay_link(
    session: AsyncSession, stripe_client: StripeClient, top_up_id: UUID
) -> str:

    urls: tuple[str, str] = (stripe_stg.stripe_success_url, stripe_stg.stripe_cancel_url)
    info: tuple[int, UUID] = await get_top_up_info(session=session, top_up_id=top_up_id)
    try:
        link: str = await generate_pay_link(
            stripe_client=stripe_client,
            top_up_id=top_up_id,
            amount=info[0],
            user_id=info[1],
            urls=urls,
        )

    except error.StripeError as e:
        raise e

    return link
