from typing import Annotated, Optional

import typer
from rich.console import Console

from alcoholic.config import load_config, save_config, VOLUME_UNITS

console = Console()


def update_settings(
    currency: Annotated[
        Optional[str],
        typer.Option(
            "--currency", "-c", help="Set the default active currency (e.g., GBP, JPY)"
        ),
    ] = None,
    unit: Annotated[
        Optional[str],
        typer.Option(
            "--unit", "-u", help="Set the default volume unit (e.g., L, ml, pt)"
        ),
    ] = None,
):
    """
    Update your default CLI configuration.
    """
    config = load_config()
    updated = False

    if currency:
        currency = currency.upper()
        config["active_currency"] = currency
        console.print(
            f"[bold green]✔[/bold green] Default currency updated to: [bold]{currency}[/bold]"
        )
        updated = True

    if unit:
        if unit not in VOLUME_UNITS:
            console.print(
                f"[bold red]Error:[/bold red] Unknown unit '{unit}'. Valid units are: {', '.join(VOLUME_UNITS.keys())}"
            )
            raise typer.Exit(code=1)
        config["default_unit"] = unit
        console.print(
            f"[bold green]✔[/bold green] Default volume unit updated to: [bold]{unit}[/bold]"
        )
        updated = True

    if updated:
        save_config(config)
    else:
        # If the user just types `alcoholic config` with no flags, show them their current setup
        console.print("[bold cyan]Current Configuration:[/bold cyan]")
        console.print(
            f"  • Currency: [bold]{config.get('active_currency', 'USD')}[/bold]"
        )
        console.print(f"  • Unit:     [bold]{config.get('default_unit', 'L')}[/bold]")
        console.print("Use --currency or --unit to make changes.")
