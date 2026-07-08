from fastapi import APIRouter

from .bind_seti_id import router as bind_seti_id
from .create_topup_request import router as create_topup_request
from .generate_seti_id import router as generate_seti_id
from .webhooks import router as webhooks

billing_router = APIRouter(prefix="/billing", tags=["billing"])
service_router = APIRouter(prefix="/service", tags=["service"])
internal_router = APIRouter(prefix="/service", tags=["internal"])


billing_router.include_router(bind_seti_id)
billing_router.include_router(create_topup_request)
service_router.include_router(generate_seti_id)
internal_router.include_router(webhooks)

__all__ = (
    "billing_router",
    "internal_router",
    "service_router",
)
