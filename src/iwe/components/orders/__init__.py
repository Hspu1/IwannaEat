from fastapi import APIRouter

from .initialize import router as initialize
from .positions import router as positions

orders_router = APIRouter(prefix="/orders", tags=["orders"])
orders_router.include_router(initialize)
orders_router.include_router(positions)

__all__ = ("orders_router",)
