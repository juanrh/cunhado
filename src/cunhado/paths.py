from pathlib import Path
import os
import tempfile

BASENAME = "cunhado"
_HOME = Path(os.environ["HOME"]) / f".{BASENAME}"
DEFAULT_SECRETS_FILE = _HOME / "secrets.env"
DEFAULT_SETTINGS_FILE = _HOME / "settings.yaml"
LOG_DIR_BASENAME = f"{BASENAME}_logs"


def temp_log_dir() -> str:
    base_temp = tempfile.gettempdir()
    log_dir = os.path.join(base_temp, LOG_DIR_BASENAME)
    os.makedirs(log_dir, exist_ok=True)
    return log_dir
