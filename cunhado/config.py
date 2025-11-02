from typing import Optional
from dataclasses import dataclass
from pathlib import Path
import os

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

_CUNHADO_HOME = Path(os.environ["HOME"])
_DEFAULT_SECRETS_FILE = _CUNHADO_HOME / ".cunhado_secrets"


class Secrets(BaseSettings):
    """Memento Tarvern config"""

    # https://docs.pydantic.dev/latest/concepts/pydantic_setting
    model_config = SettingsConfigDict(
        env_file=_DEFAULT_SECRETS_FILE,
        env_file_encoding="utf-8",
        extra="ignore",
        env_prefix="cunhado_",
    )

    mistral_api_key: Optional[str] = Field(default=None, repr=False)
    open_router_api_key: Optional[str] = Field(default=None, repr=False)


class Settings(BaseSettings): ...


@dataclass
class Config:
    secrets: Secrets
    settings: Settings


# https://docs.pydantic.dev/latest/concepts/pydantic_settings/#dotenv-env-support
def get_secrets(env_file: Path) -> Secrets:
    return Secrets(_env_file=env_file)
