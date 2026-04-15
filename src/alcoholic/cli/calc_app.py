from typing import Annotated

import typer

def calculate(
    quantity: Annotated[float, typer.Option(help="Quantity in Litres (e.g., 0.75)")],
    abv: Annotated[float, typer.Option(help="Alcohol percentage (e.g., 13.5)")],
    price: Annotated[float, typer.Option(help="Total price of the bottle/pack")]
):
    """
    Calculates the cost per litre of pure ethanol.
    """
    if quantity <= 0 or abv <= 0:
        typer.secho("Error: Quantity and ABV must be greater than zero.", fg=typer.colors.RED)
        raise typer.Exit(code=1)

    # Calculate pure alcohol volume
    pure_vol = quantity * (abv / 100)
    
    # Calculate value proposition
    value = price / pure_vol

    typer.echo("------------------------------------")
    typer.echo(f"Pure Ethanol Volume: {pure_vol:.3f} L")
    typer.secho(f"Cost per Pure Litre: ${value:.2f}", fg=typer.colors.GREEN, bold=True)
    typer.echo("------------------------------------")
