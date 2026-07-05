from pathlib import Path
from typing import Annotated

from pydantic import AfterValidator, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent.parent
ENV_FILE = BASE_DIR / ".env"
CFG = SettingsConfigDict(env_file=ENV_FILE, env_file_encoding="utf-8", extra="ignore")


class PostgresSettings(BaseSettings):
    model_config = CFG

    postgres_url: Annotated[PostgresDsn, AfterValidator(str)]
    pgbouncer_url: Annotated[PostgresDsn, AfterValidator(str)]


class StripeSettings(BaseSettings):
    model_config = CFG

    stripe_secret_key: str
    stripe_webhook_secret: str

    stripe_success_url: str = "http://127.0.0.1:1488/docs"
    stripe_cancel_url: str = "http://127.0.0.1:1488/docs"


pg_stg = PostgresSettings()
stripe_stg = StripeSettings()
