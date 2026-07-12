from fastapi import APIRouter, status

from iwe.core.dependencies import stripe_client

router = APIRouter(prefix="/generate")


@router.post("/seti-id", status_code=status.HTTP_201_CREATED)
async def generate_setup_intent() -> dict[str, str]:
    """Frontend's business actually (ts a mock)"""

    intent = await stripe_client.setup_intents.create_async()
    return {"seti-id": intent.id}
