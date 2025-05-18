from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict
import os

load_dotenv()


class Settings(BaseSettings):
    """Application settings management.

    This class uses Pydantic to handle configuration settings with validation.
    Settings can be loaded from environment variables or .env files.

    Attributes:
        DATABASE_URL (str): Database connection string.
        API_V1_STR (str): API version prefix for routes.
        PROJECT_NAME (str): Name of the project.
        BACKEND_CORS_ORIGINS (list[str]): List of allowed CORS origins.
        DEBUG (bool): Debug mode flag.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
    )

    # Database settings - must be provided via environment variables
    DATABASE_URL: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_PORT: str = "5432"
    POSTGRES_HOST: str = "localhost"

    # API settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Cinch API"
    API_PORT: str = "8000"

    # CORS settings
    BACKEND_CORS_ORIGINS: list[str] = ["*"]

    # Debug settings
    DEBUG: bool = True


settings = Settings()
