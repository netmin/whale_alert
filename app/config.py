from pathlib import Path

import yaml
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

ROOT_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    """Единый контейнер настроек проекта."""

    # --- Secrets (.env) ---
    alchemy_api_key: str | None = Field(default=None, title="Alchemy API key")
    bitquery_api_key: str | None = Field(default=None)
    telegram_bot_token: str
    telegram_chat_id: str

    # --- Общие параметры ---
    log_level: str = "INFO"
    log_json: bool = False  # переключатель «цвет ⟷ JSON»

    # --- Blockchains ---
    eth_threshold_usd: float = 500_000.0
    btc_threshold_btc: float = 50.0
    watch_addresses: list[str] = Field(default_factory=list)
    ignore_addresses: list[str] = Field(default_factory=list)

    # --- внутренние настройки Pydantic Settings ---
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", case_sensitive=False
    )


def load_yaml_cfg(path: Path) -> dict:
    if not path.exists():
        return {}
    return yaml.safe_load(path.read_text()) or {}


def load_settings() -> Settings:
    """Сливает: `.env` ▶ `config.yaml` ▶ значения по умолчанию."""
    base = Settings()  # сначала .env и дефолты
    yaml_cfg = load_yaml_cfg(ROOT_DIR / "config.yaml")
    return base.model_copy(update=yaml_cfg)  # yaml «переезжает» поверх .env


# глобальный объект конфигурации
settings = load_settings()
