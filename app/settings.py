from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""

    # General
    API_V1_STR: str = "/api/v1"

    # Database
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432

    # Application
    APP_NAME: str = "JamAndFlow - API"
    DEBUG: bool = False
    VERSION: str = "1.0.0"

    class Config:
        """Configuration for the settings."""

        env_file = ".env"
        case_sensitive = True

    @property
    def database_url(self) -> str:
        """Construct the database URL from the settings."""
        return (
            f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )


settings = Settings()
