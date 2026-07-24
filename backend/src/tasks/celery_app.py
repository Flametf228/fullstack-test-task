import asyncio

from celery import Celery

from src.core.config import settings
from src.core.logging import setup_logging

setup_logging()

_worker_loop: asyncio.AbstractEventLoop | None = None


def run_in_worker_loop(coroutine):
    global _worker_loop

    if _worker_loop is None or _worker_loop.is_closed():
        _worker_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(_worker_loop)

    return _worker_loop.run_until_complete(coroutine)


celery_app = Celery(
    "file_tasks",
    broker=settings.celery_broker,
    backend=settings.redis_backend,
    include=["src.tasks.pipeline"],
)
