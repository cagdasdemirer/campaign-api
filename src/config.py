from functools import lru_cache

from dotenv import find_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

dotenv_path = find_dotenv()
if not dotenv_path:
    raise FileNotFoundError("No .env file found in the current directory or any parent directories.")


class Settings(BaseSettings):
    APP_NAME: str = "campaign-api"
    APP_VERSION: str = "1.0.0"
    APP_PORT: int = 8000
    APP_HOST: str = "localhost"
    APP_LOG_LEVEL: str = "info"

    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USERNAME: str
    DB_PASSWORD: str
    ECHO_SQL: bool = False

    ADMIN_EMAIL: str
    ADMIN_NAME: str

    model_config = SettingsConfigDict(env_file=dotenv_path)

    @property
    def get_db_uri(self) -> str:
        return f"mysql+asyncmy://{self.DB_USERNAME}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

@lru_cache
def get_settings():
    return Settings()