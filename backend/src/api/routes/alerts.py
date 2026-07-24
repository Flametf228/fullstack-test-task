from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.deps import get_session
from src.core.config import settings
from src.repositories.alerts import AlertRepository
from src.schemas import AlertItem

router = APIRouter(prefix="/alerts", tags=["alerts"])


@router.get("", response_model=list[AlertItem])
async def list_alerts(session: AsyncSession = Depends(get_session)):
    rows = await AlertRepository(session).list(limit=settings.list_limit)
    return [AlertItem.model_validate(row) for row in rows]
