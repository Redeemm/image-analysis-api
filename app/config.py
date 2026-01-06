from typing import List, Set
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path


class Settings(BaseSettings):
    """Application settings with environment variable support"""

    # Application
    app_name: str = "Image Analysis API"
    app_version: str = "1.0.0"
    debug: bool = False
    environment: str = "development"  # development, staging, production

    # API
    api_v1_prefix: str = "/api/v1"
    cors_origins: List[str] = ["*"]

    # Server
    host: str = "0.0.0.0"
    port: int = 8000

    # Logging
    log_level: str = "INFO"  # DEBUG, INFO, WARNING, ERROR, CRITICAL

    # File Upload
    upload_dir: Path = Path("uploads")
    max_file_size: int = 5 * 1024 * 1024  # 5MB in bytes
    allowed_extensions: Set[str] = {"image/jpeg", "image/jpg", "image/png"}
    allowed_file_extensions: Set[str] = {".jpg", ".jpeg", ".png"}

    # Analysis
    mock_analysis: bool = True  # Set to False when using real ML model

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Ensure upload directory exists
        self.upload_dir.mkdir(exist_ok=True)


# Global settings instance
settings = Settings()
