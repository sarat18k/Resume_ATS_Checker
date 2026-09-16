from functools import lru_cache
from pathlib import Path

from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

PROJECT_ROOT = Path(__file__).resolve().parents[1]


class Limits(BaseModel):
    jd_text: int = 3000
    resume_text: int = 3000


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=PROJECT_ROOT / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    openai_api_key: str | None = None
    openai_model: str = "gpt-4o-mini"
    max_pdf_bytes: int = 10 * 1024 * 1024
    max_batch_resumes: int = 20
    max_concurrent_evaluations: int = 3
    ocr_enabled: bool = True
    max_ocr_pages: int = 10
    api_key: str | None = None
    rate_limit_per_minute: int = 120
    cors_origins: str = "*"
    api_prefix: str = "/api/v1"
    log_level: str = "INFO"
    limits: Limits = Field(default_factory=Limits)

    @property
    def project_root(self) -> Path:
        return PROJECT_ROOT

    @property
    def api_auth_enabled(self) -> bool:
        return bool(self.api_key and self.api_key.strip())

    def cors_origin_list(self) -> list[str]:
        if self.cors_origins.strip() == "*":
            return ["*"]
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
