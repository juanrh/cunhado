from typing import Optional
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
import os

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic_yaml import parse_yaml_raw_as

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


class ModelProvider(str, Enum):
    """Enum representing supported model providers."""

    MISTRAL = "mistral"
    OPENROUTER = "openrouter"


class Settings(BaseSettings):
    """Application settings."""

    model_provider: ModelProvider = Field(
        description="The model provider to use (mistral or openrouter)"
    )


@dataclass
class Config:
    secrets: Secrets
    settings: Settings


# https://docs.pydantic.dev/latest/concepts/pydantic_settings/#dotenv-env-support
def get_secrets(env_file: Path) -> Secrets:
    return Secrets(_env_file=env_file)


def get_settings_from_yaml(path: Path) -> Settings:
    """
    Load Settings from a YAML file.

    Args:
        path: Path to the YAML file containing settings

    Returns:
        Settings: The loaded settings object
    """
    with path.open("r", encoding="utf-8") as f:
        yaml_content = f.read()
    return parse_yaml_raw_as(Settings, yaml_content)

