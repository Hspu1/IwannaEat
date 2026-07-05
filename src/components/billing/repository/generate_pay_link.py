from uuid import UUID

from stripe import StripeClient


async def generate_pay_link(
    stripe_client: StripeClient,
    top_up_id: UUID,
    amount: int,
    user_id: UUID,
    urls: tuple[str, str],
) -> str:

    checkout_session = await stripe_client.checkout.sessions.create_async(
        params={
            "payment_method_types": ["card"],
            "line_items": [
                {
                    "price_data": {
                        "currency": "rub",
                        "product_data": {
                            "name": f"Top Up wallet #{top_up_id}",
                        },
                        "unit_amount": amount,
                    },
                    "quantity": 1,
                }
            ],
            "mode": "payment",
            "success_url": urls[0],
            "cancel_url": urls[1],
            "metadata": {"top_up_id": str(top_up_id), "user_id": str(user_id)},
        },
        options={"idempotency_key": str(top_up_id)},
    )

    return checkout_session.url
