from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    bot_token: str
    proxy_url: str | None = None

    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] | None = "INFO"
    logging_format: str = "{asctime} [{levelname}] - {name} : {message}"

    model_config = SettingsConfigDict(case_sensitive=False, env_file=".env")


settings = Settings()  # type: ignore
