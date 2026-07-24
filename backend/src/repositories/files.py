from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import StoredFile


class FileRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get(self, file_id: str) -> StoredFile | None:
        return await self.session.get(StoredFile, file_id)

    async def list(self, limit: int) -> list[StoredFile]:
        result = await self.session.execute(
            select(StoredFile).order_by(StoredFile.created_at.desc()).limit(limit)
        )
        return list(result.scalars().all())

    def add(self, file: StoredFile) -> None:
        self.session.add(file)

    async def delete(self, file: StoredFile) -> None:
        await self.session.delete(file)
