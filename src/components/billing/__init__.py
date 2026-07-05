from fastapi import APIRouter

from . import create_request, generate_link, webhooks

billing_router = APIRouter(prefix="/billing", tags=["billing"])

billing_router.include_router(create_request.router)
billing_router.include_router(generate_link.router)
billing_router.include_router(webhooks.router)

__all__ = ("billing_router",)
