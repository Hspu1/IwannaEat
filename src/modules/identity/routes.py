from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.dependencies import get_pg_session

from .usecases import register_new_user

identity_router = APIRouter(prefix="/identity")


@identity_router.post("", status_code=status.HTTP_201_CREATED)
async def register_user(session: Annotated[AsyncSession, Depends(get_pg_session)]) -> str:
    return await register_new_user(session=session)
