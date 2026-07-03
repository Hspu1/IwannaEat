from fastapi import APIRouter

from .identity import identity_router

modules_router = APIRouter()
modules_router.include_router(identity_router)

__all__ = ("modules_router",)
