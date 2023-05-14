from pydantic import BaseSettings


class Settings(BaseSettings):
    server_host: str = "0.0.0.0"
    server_port: int = 8080
    REAL_DATABASE_URL: str = "postgresql+asyncpg://postgres:password@db:5432/postgres"

settings = Settings(
    _env_file='.env',
    _env_file_encoding='utf-8',
)