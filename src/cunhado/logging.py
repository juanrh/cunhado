from pathlib import Path
import logging
import time
from typing import Protocol
from dataclasses import replace

from cunhado.config import Config
from cunhado.paths import temp_log_dir, BASENAME


def setup_logging(config: Config) -> Config:
    """Set up file logger that overwrites the log file each time"""
    settings = config.settings

    # Resolve log_dir if None
    resolved_log_dir = (
        settings.log_dir if settings.log_dir is not None else temp_log_dir()
    )

    # Resolve log_filename if None
    resolved_log_filename = settings.log_filename
    if resolved_log_filename is None:
        resolved_log_filename = f"{BASENAME}_{int(time.time())}.log"

    # Configure the root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(settings.log_level)

    # https://strandsagents.com/latest/documentation/docs/user-guide/quickstart/#debug-logs
    logging.getLogger("strands").setLevel(settings.log_level)

    # Create log directory if it doesn't exist
    log_dir = Path(resolved_log_dir)
    log_dir.mkdir(exist_ok=True)

    # Set up file handler that overwrites the file
    file_handler = logging.FileHandler(log_dir / resolved_log_filename, mode="w")
    file_handler.setLevel(logging.DEBUG)

    # Set up formatter
    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] - [%(process)d] - %(name)s:%(lineno)d - %(message)s"
    )
    file_handler.setFormatter(formatter)

    # Add handler to root logger
    root_logger.addHandler(file_handler)

    # Return modified config with resolved values
    resolved_settings = settings.model_copy(
        update={"log_dir": resolved_log_dir, "log_filename": resolved_log_filename}
    )
    return replace(config, settings=resolved_settings)


class Logging(Protocol):  # pylint: disable=too-few-public-methods
    """Adds a `log` property for the class logger to classes
    that extend this Protocol."""

    @property
    def _log(self) -> logging.Logger:
        """The logger for this class"""
        return logging.getLogger(self.__class__.__name__)
