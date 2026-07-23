from fastapi import APIRouter

from .initialize import router as initialize

orders_router = APIRouter(prefix="/orders", tags=["orders"])
orders_router.include_router(initialize)

__all__ = ("orders_router",)
