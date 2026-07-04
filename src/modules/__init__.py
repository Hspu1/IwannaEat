from fastapi import APIRouter

from .billing import billing_router
from .identity import identity_router

modules_router = APIRouter()
modules_router.include_router(identity_router)
modules_router.include_router(billing_router)

__all__ = ("modules_router",)
