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
    gcp_service_account_key_path: str


@lru_cache()
def get_settings() -> Settings:
    return Settings()


def url_slug_regex() -> str:
    return r"^[a-z0-9]+(?:-[a-z0-9]+)*$"
