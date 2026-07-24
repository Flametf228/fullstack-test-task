from fastapi import APIRouter, Depends, File, Form, UploadFile
from fastapi.responses import StreamingResponse

from src.api.deps import get_file_service
from src.schemas import FileItem, FileUpdate
from src.services.files import FileService
from src.tasks.pipeline import process_file

router = APIRouter(prefix="/files", tags=["files"])


@router.get("", response_model=list[FileItem])
async def list_files(service: FileService = Depends(get_file_service)):
    return await service.list()


@router.post("", response_model=FileItem, status_code=201)
async def create_file(
    title: str = Form(..., min_length=1, max_length=255),
    file: UploadFile = File(...),
    service: FileService = Depends(get_file_service),
):
    item = await service.create(title=title.strip(), upload_file=file)
    process_file.delay(item.id)
    return item


@router.get("/{file_id}", response_model=FileItem)
async def get_file(file_id: str, service: FileService = Depends(get_file_service)):
    return await service.get(file_id)


@router.patch("/{file_id}", response_model=FileItem)
async def update_file(
    file_id: str,
    payload: FileUpdate,
    service: FileService = Depends(get_file_service),
):
    return await service.update(file_id=file_id, title=payload.title.strip())


@router.get("/{file_id}/download")
async def download_file(file_id: str, service: FileService = Depends(get_file_service)):
    item, stream = await service.open_stream(file_id)
    return StreamingResponse(
        stream,
        media_type=item.mime_type,
        headers={
            "Content-Length": str(item.size),
            "Content-Disposition": f'attachment; filename="{item.original_name}"',
        },
    )


@router.delete("/{file_id}", status_code=204)
async def delete_file(file_id: str, service: FileService = Depends(get_file_service)):
    await service.delete(file_id)
