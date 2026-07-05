from fastapi import APIRouter

from .routes import router

identity_router = APIRouter()
identity_router.include_router(router)

__all__ = ("identity_router",)
