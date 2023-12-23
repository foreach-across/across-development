import typer

app = typer.Typer()


@app.command()
def start():
    print(f"TODO: Start release")


@app.command()
def finish():
    print(f"TODO: Finish release")


if __name__ == "__main__":
    app()
