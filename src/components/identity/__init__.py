from fastapi import APIRouter

from .register import router as register

identity_router = APIRouter()
identity_router.include_router(register)

__all__ = ("identity_router",)
