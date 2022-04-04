from pydantic import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    DEBUG: bool = False
    ECHO_ACTIVE: bool = False
    AUTH_TOKEN: str = "SPEWRsr0edwapIvgdWlKOlrXoxbcREzuSerQaTMZJ05W01c0E2Mgq-ULrRYSsjwrnZLIj4LNZ4qhC2rQCUVu5Q"
    SKIP_AUTH: bool = 0

    class Config:
        env_file = ".env"

@lru_cache
def get_settings():
    return Settings()