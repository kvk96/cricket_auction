"""Application Configuration"""
from typing import List
from pydantic_settings import BaseSettings
from pydantic import Field
from pathlib import Path
import os


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Basic
    APP_NAME: str = "Cricket Auction Platform"
    DEBUG: bool = Field(default=False, alias="DEBUG")
    ENVIRONMENT: str = Field(default="development", alias="ENVIRONMENT")
    LOG_LEVEL: str = Field(default="INFO", alias="LOG_LEVEL")

    # Backend Server
    BACKEND_HOST: str = Field(default="127.0.0.1", alias="BACKEND_HOST")
    BACKEND_PORT: int = Field(default=8000, alias="BACKEND_PORT")

    # Database
    DATABASE_URL: str = Field(
        default="postgresql+asyncpg://cricket_user:cricket_pass@localhost:5432/cricket_auction_db",
        alias="DATABASE_URL",
    )

    # JWT
    SECRET_KEY: str = Field(
        default="your-secret-key-change-in-production-min-32-chars-long",
        alias="SECRET_KEY",
    )
    ALGORITHM: str = Field(default="HS256", alias="ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=30, alias="ACCESS_TOKEN_EXPIRE_MINUTES")
    REFRESH_TOKEN_EXPIRE_DAYS: int = Field(default=7, alias="REFRESH_TOKEN_EXPIRE_DAYS")

    # CORS
    CORS_ORIGINS: List[str] = Field(
        default=["http://localhost:4200", "http://localhost:3000"],
        alias="CORS_ORIGINS",
    )
    ALLOWED_HOSTS: List[str] = Field(
        default=["localhost", "127.0.0.1"],
        alias="ALLOWED_HOSTS",
    )

    # File Upload
    UPLOAD_DIRECTORY: str = Field(default="./uploads", alias="UPLOAD_DIRECTORY")
    MAX_UPLOAD_SIZE_MB: int = Field(default=10, alias="MAX_UPLOAD_SIZE_MB")
    MAX_UPLOAD_SIZE_BYTES: int = Field(default=10 * 1024 * 1024)
    ALLOWED_IMAGE_TYPES: List[str] = Field(
        default=["jpg", "jpeg", "png", "gif", "webp"],
        alias="ALLOWED_IMAGE_TYPES",
    )
    ALLOWED_VIDEO_TYPES: List[str] = Field(
        default=["mp4", "avi", "mov", "mkv"],
        alias="ALLOWED_VIDEO_TYPES",
    )

    # Email Configuration
    SMTP_HOST: str = Field(default="smtp.gmail.com", alias="SMTP_HOST")
    SMTP_PORT: int = Field(default=587, alias="SMTP_PORT")
    SMTP_USER: str = Field(default="", alias="SMTP_USER")
    SMTP_PASSWORD: str = Field(default="", alias="SMTP_PASSWORD")
    SMTP_FROM: str = Field(default="noreply@cricketauction.local", alias="SMTP_FROM")

    # Auction Settings
    AUCTION_BASE_TIMER_SECONDS: int = 30
    AUCTION_INCREMENT_TIMER_SECONDS: int = 10
    MIN_BID_INCREMENT_PERCENTAGE: float = 0.10  # 10% minimum increment

    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"

    def __init__(self, **data):
        super().__init__(**data)
        # Calculate max upload size in bytes
        self.MAX_UPLOAD_SIZE_BYTES = self.MAX_UPLOAD_SIZE_MB * 1024 * 1024
        # Parse CORS origins if it's a string
        if isinstance(self.CORS_ORIGINS, str):
            self.CORS_ORIGINS = [origin.strip() for origin in self.CORS_ORIGINS.split(",")]
        if isinstance(self.ALLOWED_HOSTS, str):
            self.ALLOWED_HOSTS = [host.strip() for host in self.ALLOWED_HOSTS.split(",")]


settings = Settings()
