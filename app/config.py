from pydantic import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    DEBUG: bool = False
    ECHO_ACTIVE: bool = False
    AUTH_TOKEN: str = None
    SKIP_AUTH: bool = 0

    class Config:
        env_file = ".env"

@lru_cache
def get_settings():
    return Settings()