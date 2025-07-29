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

    # Security
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    # Application
    APP_NAME: str = "JamAndFlow - API"
    DEBUG: bool = False
    VERSION: str = "1.0.0"

    # Email
    FROM_EMAIL: str
    SMTP_PASSWORD: str
    SMTP_USERNAME: str
    SMTP_SERVER: str = "smtp.gmail.com"
    SMTP_PORT: int = 587

    # github
    GITHUB_CLIENT_ID: str
    GITHUB_CLIENT_SECRET: str

    # google
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str

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
