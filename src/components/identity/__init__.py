from fastapi import APIRouter

from . import register

identity_router = APIRouter()
identity_router.include_router(register.router)

__all__ = ("identity_router",)
