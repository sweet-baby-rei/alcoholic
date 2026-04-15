import typer
from alcoholic.cli.calc_app import calculate

app = typer.Typer(help="Calculate the 'Bang for your Buck' on alcohol purchases.")

app.command(calculate)


if __name__ == "__main__":
    app()