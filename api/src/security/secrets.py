import os
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    MARIADB_DATABASE: str
    MARIADB_USER: str
    MARIADB_PASSWORD: str
    MARIADB_ROOT_PASSWORD: str
    MARIADB_PORT: int
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    BCRYPT_HASH_ROUND: int
    model_config = SettingsConfigDict(env_file="api.env")

    @property
    def MARIADB_HOST(self) -> str:
        return "mariadb" if os.getenv("MODE") == "prod" else "localhost"


SECRET = Settings()
