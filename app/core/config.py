from pydantic_settings import BaseSettings
from pydantic import field_validator
from typing import List


class Settings(BaseSettings):
	app_name: str = "FastAPI CRUD"
	debug: bool = True
	database_url: str = "sqlite:///fastapi.db"
	cors_allow_origins: List[str] = ["http://localhost:3000", "*"]
	timezone: str = "Asia/Manila"  # Philippines Time (GMT+8)

	@field_validator("cors_allow_origins", mode="before")
	def ensure_list(cls, v):  # type: ignore[override]
		if isinstance(v, str):
			return [i.strip() for i in v.split(",") if i.strip()]
		return v

	class Config:
		env_file = ".env"
		env_file_encoding = "utf-8"


settings = Settings()
