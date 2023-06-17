from typing import Optional

from pydantic import BaseSettings


class Settings(BaseSettings):
    """
    TODO: override_settings in test.
    Temp Fix: hardcoded SECRET_KEY because override_settings not working
    """

    SECRET_KEY: Optional[str] = "SECRET_KEY"

    class Config:
        env_file: str = ".env"


# @lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
