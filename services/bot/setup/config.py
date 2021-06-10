import os
from functools import lru_cache
from pydantic import BaseSettings


class Settings(BaseSettings):
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    project_path: str = os.path.abspath(os.getcwd())

    project_name: str
    debug: bool
    host: str
    port: str

    telegram_session_name: str
    telegram_api_id: str
    telegram_api_hash: str
    telegram_bot_webhook_url: str
    telegram_bot_api_key: str

    database_url: str
    database_username: str
    database_password_secret: str
    database_password_secret_version: str
    database_host: str
    database_instance: str
    database_name: str

    api_v1_str: str
    api_secret_key: str

    gcp_project_id: str
    gcp_secret_id: str
    gcp_secrets_version_id: str

    zilstream_token_url: str

    cas_api_url: str


@lru_cache()
def get_settings() -> Settings:
    return Settings()
