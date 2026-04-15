import typer
from alcoholic.cli.calc_app import calculate
from alcoholic.cli.config_app import update_settings

# App 1: The Main Calculator
calc_cli = typer.Typer(help="Calculate the 'Bang for your Buck' on alcohol purchases.")
calc_cli.command()(calculate)

# App 2: The Configuration Manager
config_cli = typer.Typer(help="Configure default settings for alcoholic.")
config_cli.command()(update_settings)
