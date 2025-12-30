from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """Application settings from environment variables."""

    model_config = SettingsConfigDict(
        env_file = ".env",
        env_file_encoding = "utf-8",
        case_sensitive=False,
    )

    app_name: str = "Gymnius Vision API"
    environment: str = "development"
    debug: bool = True
    log_level: str = "DEBUG"

    host: str = "0.0.0.0"
    port: int = 8000

    # Redis
    redis_url: str = "redis://localhost:6379"


settings = Settings()
