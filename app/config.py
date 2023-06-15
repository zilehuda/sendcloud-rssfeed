from functools import lru_cache

from pydantic import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    SECRET_KEY: Optional[
        str
    ] = "SECRET_KEY"  # TODO: override_settings in test. Temp Fix: hardcoded SECRET_KEY because override_settings not working

    class Config:
        env_file: str = ".env"


# @lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
