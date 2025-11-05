import logging
from pathlib import Path
from typing import Annotated

from cyclopts import App, Parameter

from cunhado.config import get_config, Config
from cunhado.logging import setup_logging
from cunhado.paths import DEFAULT_SECRETS_FILE, DEFAULT_SETTINGS_FILE

_LOG = logging.getLogger(__name__)

app = App(help="Your cuñado thinks he's an expert on everything")
app.command(chat := App(name="chat"))


def setup_app(secrets_env_file: Path, settings_file: Path) -> Config:
    config = get_config(secrets_env_file=secrets_env_file, settings_file=settings_file)
    config = setup_logging(config)
    print(f"Using log file '{config.log_file}'")
    return config


@app.default  # Runs as `cunhado`
@chat.default  # Runs as `cunhado chat`
@chat.command(name="start")  # Runs as `cunhado chat start`
def start_chat(
    #    *, # This disables specifying parameters with env vars
    secrets: Annotated[
        Path, Parameter(name=["--secrets", "-sc"])
    ] = DEFAULT_SECRETS_FILE,
    settings: Annotated[
        Path, Parameter(name=["--settings", "-st"])
    ] = DEFAULT_SETTINGS_FILE,
):
    """
    Start a chat

    Parameters
    ----------
    secrets: Path
        Path of the secrets env file.
    settings: Path
        Path of the settings YAML file.
    """
    config = setup_app(secrets_env_file=secrets, settings_file=settings)
    _LOG.info(f"Using secrets: '{secrets}', settings: '{settings}', config: '{config}'")
    print("bye")
