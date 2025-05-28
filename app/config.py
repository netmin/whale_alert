from pathlib import Path

import yaml
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

ROOT_DIR = Path(__file__).resolve().parent.parent


class SourcesSettings(BaseModel):
    eth_infura: bool = False
    btc_ws: bool = False
    bitquery: bool = False


class Settings(BaseSettings):

    alchemy_api_key: str | None = Field(default=None, title="Alchemy API key")
    bitquery_api_key: str | None = Field(default=None)
    telegram_bot_token: str | None = None
    telegram_chat_id: str | None = None

    log_level: str = "DEBUG"
    log_json: bool = False

    eth_threshold_usd: float = 500_000.0
    btc_threshold_btc: float = 50.0
    watch_addresses: list[str] = Field(default_factory=list)
    ignore_addresses: list[str] = Field(default_factory=list)

    sources: SourcesSettings = Field(default_factory=SourcesSettings)

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", case_sensitive=False
    )


def load_yaml_cfg(path: Path) -> dict:
    if not path.exists():
        return {}
    return yaml.safe_load(path.read_text()) or {}


def load_settings() -> Settings:
    base = Settings()
    yaml_cfg = load_yaml_cfg(ROOT_DIR / "config.yaml")
    return base.model_copy(update=yaml_cfg)


settings = load_settings()
