import urllib.request
import json
from typing import Annotated, Optional

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from alcoholic.config import load_config, get_verdict, get_locale, VOLUME_UNITS, FALLBACK_RATES, CURRENCY_THRESHOLDS

console = Console()

def get_exchange_rate(target: str, offline: bool) -> float:
    """Gets live rate, falls back to stale hardcoded rate, defaults to 1.0."""
    target = target.upper()
    if target == "USD": 
        return 1.0
        
    if not offline:
        try:
            url = "https://open.er-api.com/v6/latest/USD"
            with urllib.request.urlopen(url, timeout=1.5) as response:
                data = json.loads(response.read().decode())
                return data["rates"].get(target, FALLBACK_RATES.get(target, 1.0))
        except Exception:
            pass # Silently fail over to offline logic
            
    return FALLBACK_RATES.get(target, 1.0)


def calculate(
    # 1. POSITIONAL Arguments (Now Optional so flags can be used instead)
    pos_price: Annotated[Optional[float], typer.Argument(metavar="PRICE", help="Total price (Positional)")] = None,
    pos_quantity: Annotated[Optional[float], typer.Argument(metavar="QUANTITY", help="Volume quantity (Positional)")] = None,
    
    # 2. KEYWORD Options (For explicit/legacy usage)
    opt_price: Annotated[Optional[float], typer.Option("--price", "-p", help="Total price (Flag)")] = None,
    opt_quantity: Annotated[Optional[float], typer.Option("--quantity", "-q", help="Volume quantity (Flag)")] = None,
    
    # 3. Standard Overrides
    abv: Annotated[Optional[float], typer.Option("--abv", "-a", help="Alcohol percentage (e.g., 13.5)")] = None,
    unit: Annotated[Optional[str], typer.Option("--unit", "-u", help="Override default volume unit")] = None,
    currency: Annotated[Optional[str], typer.Option("--currency", "-c", help="Currency code (e.g., USD, JPY, GBP)")] = None,
    offline: Annotated[bool, typer.Option("--offline", help="Skip live API conversion")] = False,
    
    # 4. Smart Drink Flags
    beer: Annotated[bool, typer.Option("--beer", help="Evaluate as Beer (Defaults 5% ABV, 0.5L)")] = False,
    cider: Annotated[bool, typer.Option("--cider", help="Evaluate as Cider (Defaults 5% ABV, 0.5L)")] = False,
    wine: Annotated[bool, typer.Option("--wine", help="Evaluate as Wine (Defaults 13% ABV, 0.75L)")] = False,
    mid_strength: Annotated[bool, typer.Option("--liqueur", "--sake", "--soju", "--port", help="Evaluate as Liqueur (Defaults 20% ABV, 0.7L)")] = False,
    spirit: Annotated[bool, typer.Option("--spirit", "--vodka", "--rum", "--whiskey", "-s", help="Evaluate as Spirit (Defaults 40% ABV, 0.7L)")] = False
):
    """
    Calculates the cost per pure unit of ethanol.
    """
    config = load_config()
    lang = get_locale(config.get("language", "en"))
    
    # --- HYBRID RECONCILIATION LOGIC ---
    # Positional takes priority if both are accidentally provided
    price = opt_price
    quantity = opt_quantity
    
    # Process positional arguments intelligently
    if pos_price is not None:
        if price is None:
            # No --price flag was used, so the first positional IS the price
            price = pos_price
            if pos_quantity is not None:
                quantity = pos_quantity
        else:
            # The --price flag WAS used! So this stray positional must be the quantity
            quantity = pos_price
            
    if price is None:
        console.print("[bold red]Error:[/bold red] You must provide a price (e.g., `alcoholic 20` or `alcoholic --price 20`).")
        raise typer.Exit(code=1)
    # -----------------------------------
    
    # Resolve active unit and currency
    active_unit = unit if unit else config.get("default_unit", "L")
    active_currency = (currency if currency else config.get("active_currency", "USD")).upper()

    if active_unit not in VOLUME_UNITS:
        console.print(f"[bold red]{lang.get('error_unit', 'Error')}:[/bold red] {active_unit}")
        raise typer.Exit(code=1)

    # Resolve Category, Default ABV, AND Default Quantity
    category = "generic"
    inferred_abv = None
    inferred_qty = None

    if beer or cider:
        category = "beer_cider"
        inferred_abv = 5.0
        inferred_qty = 0.5   # 500ml can/bottle
    elif wine:
        category = "wine"
        inferred_abv = 12
        inferred_qty = 0.75  # 75cl standard wine bottle
    elif mid_strength:
        category = "mid_strength"
        inferred_abv = 20.0
        inferred_qty = 0.70  # 70cl standard liqueur bottle
    elif spirit:
        category = "spirit"
        inferred_abv = 40.0
        inferred_qty = 0.70  # 70cl standard UK spirit bottle

    # Final Validation for both ABV and Quantity
    final_abv = abv if abv is not None else inferred_abv
    final_qty = quantity if quantity is not None else inferred_qty
    
    if final_abv is None or final_qty is None:
        console.print("[bold red]Error:[/bold red] You must provide a Quantity and ABV, OR use a smart drink flag (e.g., --wine).")
        raise typer.Exit(code=1)

    if final_qty <= 0 or final_abv <= 0:
        console.print(f"[bold red]Error:[/bold red] Quantity and ABV must be greater than zero.")
        raise typer.Exit(code=1)

    # Base Math
    pure_vol = final_qty * (final_abv / 100)
    local_cost_per_pure = price / pure_vol

    # Smart Threshold Evaluation (Category + Currency)
    if active_currency in CURRENCY_THRESHOLDS:
        eval_cost = local_cost_per_pure
        currency_data = CURRENCY_THRESHOLDS[active_currency]
        symbol = currency_data.get("symbol", f"{active_currency} ")
        # Fallback to generic if the specific category isn't defined for this currency
        thresholds = currency_data.get(category, currency_data.get("generic"))
    else:
        # Fallback to API + USD Baseline thresholds
        rate = get_exchange_rate(active_currency, offline)
        eval_cost = local_cost_per_pure / rate
        currency_data = CURRENCY_THRESHOLDS["USD"]
        symbol = f"{active_currency} " 
        thresholds = currency_data.get(category, currency_data.get("generic"))

    # Determine the rating based on the thresholds
    if eval_cost < thresholds["excellent_under"]:
        rating = "excellent"
    elif eval_cost < thresholds["good_under"]:
        rating = "good"
    elif eval_cost < thresholds["average_under"]:
        rating = "average"
    else:
        rating = "expensive"

    # Fetch the nuanced template string
    verdict_text = get_verdict(category, rating)

    # UI Rendering
    table = Table(show_header=False, box=None)
    table.add_column("Metric", style="cyan")
    table.add_column("Value", justify="right")
    
    # Add indicators if we inferred the data
    abv_display = f"{final_abv:.1f}% ABV" + (" [dim](inferred)[/dim]" if abv is None else "")
    qty_display = f"{final_qty:.2f} {active_unit}" + (" [dim](inferred)[/dim]" if quantity is None else "")
    
    table.add_row("Receipt Summary:", f"{qty_display} @ {abv_display} for {symbol}{price:.2f}")
    table.add_row("Pure Ethanol Volume:", f"{pure_vol:.3f} {active_unit}")
    table.add_row(f"Cost per Pure {active_unit}:", f"[bold green]{symbol}{local_cost_per_pure:.2f}[/bold green]")
    
    if active_currency not in CURRENCY_THRESHOLDS:
        table.add_row("[dim]Evaluated against:[/dim]", f"[dim]USD Base (${eval_cost:.2f})[/dim]")
        
    table.add_row("Verdict:", verdict_text)

    panel = Panel(
        table, 
        expand=False, 
        border_style="blue"
    )
    console.print(panel)