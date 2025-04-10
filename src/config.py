import os

from pydantic_settings import BaseSettings, SettingsConfigDict

ENVIRONMENT_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")


class ProjectSettings(BaseSettings):
    """Класс конфигурации API."""

    # MARK: Project
    VERSION: str = "0.0.1"

    # MARK: Database
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: str

    ENV: str
    APP_PORT: str

    # MARK: TronAPI
    TRON_API_KEY: str

    @property
    def POSTGRESQL_URL(self):
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    model_config = SettingsConfigDict(
        env_file=ENVIRONMENT_FILE,
        extra="allow",
    )


project_settings = ProjectSettings()
