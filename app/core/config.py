from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "FastAPI Level 2 Example"
    DATABASE_URL: str = "sqlite:///./fastapi.db"

settings = Settings()