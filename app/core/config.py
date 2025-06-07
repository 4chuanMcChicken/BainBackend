from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import PostgresDsn, field_validator
from typing import Optional


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", case_sensitive=True)

    # API Settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Distance Calculator API"

    # Database
    POSTGRES_HOST: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_PORT: str = "5432"
    DATABASE_URL: Optional[PostgresDsn] = None

    # Nominatim
    NOMINATIM_USER_AGENT: str = "DistanceCalculator/1.0"
    NOMINATIM_BASE_URL: str = "https://nominatim.openstreetmap.org"

    @field_validator("DATABASE_URL", mode="before")
    def assemble_db_url(cls, v: Optional[str], values) -> str:
        if v:
            return v
        
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            username=values.data["POSTGRES_USER"],
            password=values.data["POSTGRES_PASSWORD"],
            host=values.data["POSTGRES_HOST"],
            port=int(values.data["POSTGRES_PORT"]),
            path=values.data["POSTGRES_DB"],
        )


settings = Settings() 