import logging

from cyclopts import App

from cunhado.config import get_config
from cunhado.logging import setup_logging

app = App()


@app.default
def main():
    """
    Your cuñado thinks he's an expert on everything
    """
    config = get_config()
    # TODO: add args for secrets and settings
    setup_logging(config)
    log = logging.getLogger(__name__)
    log.info(f"Using config: '{config}'")
    log.info("Hello from cunhado!")
