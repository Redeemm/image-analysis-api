from typing import List, Set
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path


class Settings(BaseSettings):
    """Application settings loaded from environment variables or .env file"""

    # Application
    app_name: str
    app_version: str
    debug: bool
    environment: str

    # API
    api_v1_prefix: str
    api_key: str
    cors_origins: List[str]

    # Server
    host: str
    port: int

    # Logging
    log_level: str

    # File Upload
    upload_dir: Path
    max_file_size: int
    allowed_extensions: Set[str]
    allowed_file_extensions: Set[str]

    # Analysis
    mock_analysis: bool

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
