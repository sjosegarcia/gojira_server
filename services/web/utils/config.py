import os
from functools import lru_cache
from pydantic import BaseSettings


class Settings(BaseSettings):
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    project_path: str = os.path.abspath(os.getcwd())

    debug: bool = True
    project_name: str
    server_name: str
    server_host: str
    server_port: str
    api_v1_str: str
    api_secret_key: str

    database_user: str
    database_password: str
    database_db: str
    database_port: str
    database_host: str
    database_socket: str
    database_url: str


@lru_cache()
def get_settings() -> Settings:
    return Settings()
