from fastapi import APIRouter

from .create_request import router as create_request_router
from .generate_link import router as generate_link_router

billing_router = APIRouter(prefix="/billing", tags=["billing"])
billing_router.include_router(create_request_router)
billing_router.include_router(generate_link_router)

__all__ = ("billing_router",)
