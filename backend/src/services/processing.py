import logging

from sqlalchemy.ext.asyncio import AsyncSession

from src.domain import alerts, metadata, scanner
from src.repositories.alerts import AlertRepository
from src.repositories.files import FileRepository
from src.storage.backend import StorageBackend

logger = logging.getLogger(__name__)


async def process_file(
    session: AsyncSession,
    storage: StorageBackend,
    file_id: str,
    *,
    record_failure: bool = True,
) -> None:
    files = FileRepository(session)
    alerts_repo = AlertRepository(session)

    row = await files.get(file_id)
    if row is None:
        logger.warning("File %s no longer exists, skipping", file_id)
        return

    try:
        row.processing_status = "processing"
        await session.commit()

        result = scanner.scan(row.original_name, row.size, row.mime_type)
        data = await storage.read(row.stored_name)
        meta = metadata.extract(row.original_name, row.size, row.mime_type, data)

        row.scan_status = result.status
        row.scan_details = result.details
        row.requires_attention = result.requires_attention
        row.metadata_json = meta
        row.processing_status = "processed"

        level, message = alerts.decide(
            row.processing_status, row.requires_attention, row.scan_details
        )
        alerts_repo.add(file_id, level, message)
        await session.commit()
        logger.info("File %s processed with scan status %s", file_id, result.status)
    except Exception as exc:
        logger.exception("Processing failed for file %s", file_id)
        await session.rollback()

        if record_failure:
            await _mark_failed(session, file_id, str(exc))

        raise


async def _mark_failed(session: AsyncSession, file_id: str, reason: str) -> None:
    files = FileRepository(session)
    alerts_repo = AlertRepository(session)

    row = await files.get(file_id)
    if row is None:
        return

    row.processing_status = "failed"
    row.scan_status = row.scan_status or "failed"
    row.scan_details = f"processing failed: {reason}"[:500]

    level, message = alerts.decide("failed", row.requires_attention, row.scan_details)
    alerts_repo.add(file_id, level, message)
    await session.commit()
