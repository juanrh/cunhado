from pathlib import Path
import logging
from typing import Protocol

from cunhado.config import Config


def setup_logging(config: Config):
    """Set up file logger that overwrites the log file each time"""
    settings = config.settings
    # Configure the root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(settings.log_level)

    # https://strandsagents.com/latest/documentation/docs/user-guide/quickstart/#debug-logs
    logging.getLogger("strands").setLevel(settings.log_level)

    # Create log directory if it doesn't exis
    log_dir = Path(settings.log_dir)
    log_dir.mkdir(exist_ok=True)

    # Set up file handler that overwrites the file
    file_handler = logging.FileHandler(log_dir / settings.log_filename, mode="w")
    file_handler.setLevel(logging.DEBUG)

    # Set up formatter
    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] - [%(process)d] - %(name)s:%(lineno)d - %(message)s"
    )
    file_handler.setFormatter(formatter)

    # Add handler to root logger
    root_logger.addHandler(file_handler)


class Logging(Protocol):  # pylint: disable=too-few-public-methods
    """Adds a `log` property for the class logger to classes
    that extend this Protocol."""

    @property
    def _log(self) -> logging.Logger:
        """The logger for this class"""
        return logging.getLogger(self.__class__.__name__)
