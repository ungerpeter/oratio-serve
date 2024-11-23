from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    MODEL_NAME: str = "nvidia/canary-1b"
    TIMEOUT_DURATION: int = 300
    LOG_LEVEL: str = "INFO"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()