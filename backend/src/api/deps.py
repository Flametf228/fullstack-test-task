from collections.abc import AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.engine import async_session_maker
from src.services.files import FileService
from src.storage.backend import StorageBackend, storage


async def get_session() -> AsyncGenerator[AsyncSession]:
    async with async_session_maker() as session:
        yield session


def get_storage() -> StorageBackend:
    return storage


def get_file_service(
    session: AsyncSession = Depends(get_session),
    store: StorageBackend = Depends(get_storage),
) -> FileService:
    return FileService(session, store)
