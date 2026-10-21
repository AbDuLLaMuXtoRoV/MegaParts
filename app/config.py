from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str = "postgresql+psycopg://megaparts:megaparts@localhost:5432/megaparts"
    api_prefix: str = "/api/v1"
    pilot_mode: bool = False
    search_debug: bool = False
    offer_fresh_hours: float = 2
    offer_recent_hours: float = 24
    preferred_supplier_ids: str = ""
    # Admin pages and /api/admin stay locked until ADMIN_PASSWORD is set.
    admin_username: str = "irizon"
    admin_password: str = ""
    session_secret: str = ""
    admin_session_hours: float = 12
    # Set true when served over HTTPS so the session cookie is never sent in clear text.
    secure_cookies: bool = False

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    return Settings()
