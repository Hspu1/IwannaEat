from collections.abc import AsyncGenerator

from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession

from src.shared.postgres.manager import PostgresManager


async def get_pg_session(request: Request) -> AsyncGenerator[AsyncSession, None]:
    pg_manager: PostgresManager = request.app.state.pg_manager
    session_maker = pg_manager.get_session_maker()

    async with session_maker.begin() as session:
        yield session
