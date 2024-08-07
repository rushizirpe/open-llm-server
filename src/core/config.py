from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "Open LLM Server"
    PROJECT_VERSION: str = "1.0.0"
    HUGGING_FACE_TOKEN: Optional[str] = None

    class Config:
        env_file = ".env"

settings = Settings()

# Add this line to ensure 'settings' is exported
__all__ = ['settings']