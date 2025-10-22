from cyclopts import App

app = App()

@app.default
def main():
    """
    Your cuñado thinks he's an expert on everything
    """
    print("Hello from cunhado!")
