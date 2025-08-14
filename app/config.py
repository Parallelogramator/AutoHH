from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    DATABASE_URL: str
    GOOGLE_API_KEY: str # Заменили ключ
    HH_API_TOKEN: str
    EMBED_INDEX_PATH: str = "/data/faiss_indices"
    AUTO_APPLY: bool = False
    REQUIRE_REVIEW: bool = True
    RUN_MODE: str = "api" # 'api' or 'worker'

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

@lru_cache
def get_settings() -> Settings:
    return Settings()