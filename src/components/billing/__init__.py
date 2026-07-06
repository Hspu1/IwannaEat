from fastapi import APIRouter

from .create_request import router as create_request
from .generate_link import router as generate_link
from .webhooks import router as webhooks

billing_router = APIRouter(prefix="/billing", tags=["billing"])

billing_router.include_router(create_request)
billing_router.include_router(generate_link)
billing_router.include_router(webhooks)

__all__ = ("billing_router",)
