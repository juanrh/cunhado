from cyclopts import App

from cunhado.config import get_config

app = App()


@app.default
def main():
    """
    Your cuñado thinks he's an expert on everything
    """
    config = get_config()
    # TODO:  use logger
    # TODO: add args for secrets and settings
    print(config)
    print("Hello from cunhado!")
