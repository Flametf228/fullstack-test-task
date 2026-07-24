from src.db.engine import async_session_maker
from src.services.processing import process_file as run_processing
from src.storage.backend import storage
from src.tasks.celery_app import celery_app, run_in_worker_loop

MAX_RETRIES = 3


async def _run(file_id: str, record_failure: bool) -> None:
    async with async_session_maker() as session:
        await run_processing(session, storage, file_id, record_failure=record_failure)


@celery_app.task(
    bind=True,
    name="src.tasks.pipeline.process_file",
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_jitter=True,
    max_retries=MAX_RETRIES,
)
def process_file(self, file_id: str) -> None:
    is_final_attempt = self.request.retries >= MAX_RETRIES
    run_in_worker_loop(_run(file_id, record_failure=is_final_attempt))
