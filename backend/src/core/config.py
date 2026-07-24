from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(extra="ignore")

    postgres_user: str = "postgres"
    postgres_password: str = "postgres"
    postgres_host: str = "backend-db"
    pgport: int = 5433
    postgres_db: str = "test"

    celery_broker_url: str = "redis://backend-redis:6379/0"

    s3_endpoint_url: str = "http://backend-minio:9000"
    s3_access_key: str = "minioadmin"
    s3_secret_key: str = "minioadmin"
    s3_bucket: str = "files"
    s3_region: str = "us-east-1"

    max_upload_size: int = 50 * 1024 * 1024
    chunk_size: int = 1024 * 1024
    list_limit: int = 200

    cors_origins: list[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ]
    log_level: str = "INFO"

    @property
    def db_url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.pgport}/{self.postgres_db}"
        )

    @property
    def celery_broker(self) -> str:
        return self.celery_broker_url

    @property
    def redis_backend(self) -> str:
        return self.celery_broker_url


settings = Settings()
