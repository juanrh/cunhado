from cyclopts import App

app = App()

@app.default
def main():
    print("Hello from cunhado!")


if __name__ == "__main__":
    app()
