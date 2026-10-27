"""
NativeSlide AI — Application Configuration
Centralised Pydantic BaseSettings for the FastAPI backend.
All values are loaded from environment variables / .env file.
"""
from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    # ── Application ────────────────────────────────────────────────────────
    APP_NAME: str = "NativeSlide AI"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False

    # Origins allowed to call the API (CORS)
    ALLOWED_ORIGINS: list[str] = Field(
        default=["http://localhost:3000", "https://nativeslide.pages.dev"],
        description="List of allowed CORS origins.",
    )

    # ── Google Gemini ──────────────────────────────────────────────────────
    GEMINI_API_KEY: str = Field(
        default="",
        description="Google AI Studio API key (https://aistudio.google.com/).",
    )
    GEMINI_MODEL: str = Field(
        default="gemini-3.5-flash",
        description="Gemini model identifier to use for slide planning.",
    )
    GEMINI_MAX_TOKENS: int = Field(
        default=8192,
        description="Maximum output tokens for a single Gemini generation call.",
    )

    # ── Supabase ───────────────────────────────────────────────────────────
    SUPABASE_URL: str = Field(
        default="",
        description="Supabase project URL (e.g. https://xxxx.supabase.co).",
    )
    SUPABASE_SERVICE_KEY: str = Field(
        default="",
        description="Supabase service-role secret key (server-side only).",
    )

    # ── Generation Limits ──────────────────────────────────────────────────
    MAX_PDF_SIZE_MB: int = Field(
        default=25,
        description="Maximum allowed PDF upload size in megabytes.",
    )
    MAX_SLIDES: int = Field(
        default=40,
        description="Absolute maximum number of slides per deck.",
    )
    FREE_TIER_MAX_SLIDES: int = Field(
        default=15,
        description="Maximum slides available on the free tier.",
    )

    # ── Storage ────────────────────────────────────────────────────────────
    OUTPUT_DIR: Path = Field(
        default=Path("/tmp/nativeslide_outputs"),
        description="Directory where generated .pptx files are temporarily stored.",
    )

    # ── Rate Limiting ──────────────────────────────────────────────────────
    RATE_LIMIT_PER_MINUTE: int = Field(
        default=10,
        description="Maximum API requests allowed per user per minute.",
    )

    # ── JWT Authentication ─────────────────────────────────────────────────
    JWT_SECRET: str = Field(
        default="nativeslide_dev_jwt_secret_change_in_production",
        description="Secret key for signing JWTs (generate with: openssl rand -hex 32).",
    )
    JWT_ALGORITHM: str = Field(
        default="HS256",
        description="Algorithm used for JWT signing.",
    )
    JWT_EXPIRE_MINUTES: int = Field(
        default=60 * 24 * 7,  # 7 days
        description="JWT token expiry time in minutes.",
    )


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """
    Return the cached application settings singleton.
    The @lru_cache ensures the .env file is parsed only once per process,
    making this safe and efficient to call anywhere in the codebase.
    """
    return Settings()  # type: ignore[call-arg]
