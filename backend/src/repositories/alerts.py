from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import Alert


class AlertRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def list(self, limit: int) -> list[Alert]:
        result = await self.session.execute(
            select(Alert).order_by(Alert.created_at.desc()).limit(limit)
        )
        return list(result.scalars().all())

    def add(self, file_id: str, level: str, message: str) -> Alert:
        alert = Alert(file_id=file_id, level=level, message=message)
        self.session.add(alert)
        return alert

    async def delete_by_file(self, file_id: str) -> None:
        await self.session.execute(delete(Alert).where(Alert.file_id == file_id))
