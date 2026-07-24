from collections.abc import AsyncIterator
from typing import BinaryIO, Protocol

import aioboto3
from botocore.config import Config
from botocore.exceptions import ClientError

from src.core.config import settings
from src.core.exceptions import StoredFileMissing


class StorageBackend(Protocol):
    async def ensure_bucket(self) -> None: ...

    async def upload(self, key: str, stream: BinaryIO, content_type: str) -> None: ...

    async def ensure_object(self, key: str) -> None: ...

    def download(self, key: str) -> AsyncIterator[bytes]: ...

    async def read(self, key: str) -> bytes: ...

    async def delete(self, key: str) -> None: ...


class S3StorageBackend:
    def __init__(self) -> None:
        self._session = aioboto3.Session()
        self._bucket = settings.s3_bucket
        self._config = Config(response_checksum_validation="when_required")

    def _client(self):
        return self._session.client(
            "s3",
            endpoint_url=settings.s3_endpoint_url,
            aws_access_key_id=settings.s3_access_key,
            aws_secret_access_key=settings.s3_secret_key,
            region_name=settings.s3_region,
            config=self._config,
        )

    async def ensure_bucket(self) -> None:
        async with self._client() as s3:
            try:
                await s3.head_bucket(Bucket=self._bucket)
            except ClientError:
                await s3.create_bucket(Bucket=self._bucket)

    async def upload(self, key: str, stream: BinaryIO, content_type: str) -> None:
        async with self._client() as s3:
            await s3.upload_fileobj(
                stream,
                self._bucket,
                key,
                ExtraArgs={"ContentType": content_type},
            )

    async def ensure_object(self, key: str) -> None:
        async with self._client() as s3:
            try:
                await s3.head_object(Bucket=self._bucket, Key=key)
            except ClientError as exc:
                raise StoredFileMissing() from exc

    async def download(self, key: str) -> AsyncIterator[bytes]:
        async with self._client() as s3:
            try:
                response = await s3.get_object(Bucket=self._bucket, Key=key)
            except ClientError as exc:
                raise StoredFileMissing() from exc

            async for chunk in response["Body"].iter_chunks(settings.chunk_size):
                yield chunk

    async def read(self, key: str) -> bytes:
        async with self._client() as s3:
            try:
                response = await s3.get_object(Bucket=self._bucket, Key=key)
            except ClientError as exc:
                raise StoredFileMissing() from exc

            return await response["Body"].read()

    async def delete(self, key: str) -> None:
        async with self._client() as s3:
            await s3.delete_object(Bucket=self._bucket, Key=key)


storage: S3StorageBackend = S3StorageBackend()
