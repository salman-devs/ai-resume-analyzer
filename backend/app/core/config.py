from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    GEMINI_API_KEY: str
    ALLOWED_ORIGINS: str = "http://localhost:5173"
    REDIS_URL: str = "redis://localhost:6379/0"
    ADZUNA_APP_ID: str = ""
    ADZUNA_APP_KEY: str = ""

    @property
    def origins(self) -> List[str]:
        return [o.strip() for o in self.ALLOWED_ORIGINS.split(",")]

    class Config:
        env_file = ".env"


settings = Settings()