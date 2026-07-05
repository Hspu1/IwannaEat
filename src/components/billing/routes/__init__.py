from fastapi import APIRouter

from .create_request import create_request_router
from .generate_link import generate_link_router

billing_router = APIRouter(prefix="/billing")
billing_router.include_router(create_request_router)
billing_router.include_router(generate_link_router)
