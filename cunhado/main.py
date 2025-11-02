from pathlib import Path

from cyclopts import App

from cunhado.config import get_secrets

app = App()


@app.default
def main():
    """
    Your cuñado thinks he's an expert on everything
    """
    secrets = get_secrets(env_file=Path("cunhado_secrets.env.example"))
    print(secrets)
    print("Hello from cunhado!")
