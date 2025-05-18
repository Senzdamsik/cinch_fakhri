from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

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

    # Database settings
    DATABASE_URL: str = "sqlite:///./app.db"

    # API settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Cinch API"

    # CORS settings
    BACKEND_CORS_ORIGINS: list[str] = ["*"]

    # Debug settings
    DEBUG: bool = True


settings = Settings()
