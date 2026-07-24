import mimetypes
from collections.abc import AsyncIterator
from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.config import settings
from src.core.exceptions import EmptyFile, FileNotFound, FileTooLarge
from src.models import StoredFile
from src.repositories.alerts import AlertRepository
from src.repositories.files import FileRepository
from src.schemas import FileItem
from src.storage.backend import StorageBackend


class FileService:
    def __init__(self, session: AsyncSession, storage: StorageBackend) -> None:
        self.session = session
        self.storage = storage
        self.files = FileRepository(session)
        self.alerts = AlertRepository(session)

    async def list(self) -> list[FileItem]:
        rows = await self.files.list(limit=settings.list_limit)
        return [FileItem.model_validate(row) for row in rows]

    async def get(self, file_id: str) -> FileItem:
        return FileItem.model_validate(await self._require(file_id))

    async def create(self, title: str, upload_file: UploadFile) -> FileItem:
        size = await self._measure(upload_file)

        file_id = str(uuid4())
        original_name = upload_file.filename or file_id
        stored_name = f"{file_id}{Path(original_name).suffix}"
        mime_type = (
            upload_file.content_type
            or mimetypes.guess_type(stored_name)[0]
            or "application/octet-stream"
        )

        await upload_file.seek(0)
        await self.storage.upload(stored_name, upload_file.file, mime_type)

        row = StoredFile(
            id=file_id,
            title=title,
            original_name=original_name,
            stored_name=stored_name,
            mime_type=mime_type,
            size=size,
            processing_status="uploaded",
        )
        self.files.add(row)
        await self.session.commit()
        await self.session.refresh(row)
        return FileItem.model_validate(row)

    async def update(self, file_id: str, title: str) -> FileItem:
        row = await self._require(file_id)
        row.title = title
        await self.session.commit()
        await self.session.refresh(row)
        return FileItem.model_validate(row)

    async def delete(self, file_id: str) -> None:
        row = await self._require(file_id)
        stored_name = row.stored_name

        await self.alerts.delete_by_file(file_id)
        await self.files.delete(row)
        await self.session.commit()
        await self.storage.delete(stored_name)

    async def open_stream(self, file_id: str) -> tuple[FileItem, AsyncIterator[bytes]]:
        row = await self._require(file_id)
        await self.storage.ensure_object(row.stored_name)
        return FileItem.model_validate(row), self.storage.download(row.stored_name)

    async def _require(self, file_id: str) -> StoredFile:
        row = await self.files.get(file_id)
        if row is None:
            raise FileNotFound()
        return row

    async def _measure(self, upload_file: UploadFile) -> int:
        size = 0
        await upload_file.seek(0)

        while chunk := await upload_file.read(settings.chunk_size):
            size += len(chunk)
            if size > settings.max_upload_size:
                raise FileTooLarge()

        if size == 0:
            raise EmptyFile()

        return size
