"""Configuration"""

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Settings"""

    app_name: str = "HR Service"
    LOG_LEVEL: str = "INFO"

    DATABASE_URL: str = Field(..., env="DATABASE_URL")
    REDIS_HOST: str = Field(..., env="REDIS_HOST")
    REDIS_PORT: int = Field(..., env="REDIS_PORT")

    class Config:
        """Config"""

        env_file = "app.env"
        env_file_encoding = "utf-8"


settings = Settings()
