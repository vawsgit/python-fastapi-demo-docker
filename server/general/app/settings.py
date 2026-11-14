import sys

from pydantic import Field, PostgresDsn, ValidationError
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(extra="ignore")
    database_url: PostgresDsn  # required
    bedrock_model_id: str = Field(min_length=1)  # required
    aws_region: str = "us-west-2"  # optional, safe everywhere
    log_level: str = "INFO"  # optional, safe everywhere


def load() -> Settings:
    try:
        return Settings()
    except ValidationError as e:
        names = ", ".join(str(err["loc"][0]).upper() for err in e.errors())
        sys.stderr.write(f"config error: missing or invalid {names}\n")
        raise SystemExit(2)


settings = load()
