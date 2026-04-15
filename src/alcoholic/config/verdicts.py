def get_verdict(category: str, rating: str) -> str:
    """
    Returns a nuanced explanation based on the category and price rating.
    Rating can be: "excellent", "good", "average", "expensive"
    """
    
    # Format the category name for display (e.g., "beer_cider" -> "Beer & Cider")
    cat_name = category.replace("_", " & ").title() if category != "generic" else "Alcohol"
    
    templates = {
        "generic": {
            "excellent": "[bold green]Excellent[/bold green] (A steal, even for bottom-shelf spirits!)",
            "good": "[bold blue]Good Price 🍻[/bold blue]",
            "average": "[bold yellow]Average 🤷[/bold yellow]\n[dim]Good deal for beer/cider, slightly overpriced for cheap spirits.[/dim]",
            "expensive": "[bold red]Expensive 💸[/bold red] (Justifiable for craft beer or premium spirits)"
        },
        "beer_cider": {
            "excellent": "[bold green]Excellent Deal 🏆[/bold green]\n[dim]This is cheaper than standard supermarket multi-packs.[/dim]",
            "good": "[bold blue]Good Price 🍻[/bold blue]\n[dim]Solid value for standard beer or cider.[/dim]",
            "average": "[bold yellow]Average 🤷[/bold yellow]\n[dim]Standard pub/bar price, or slightly pricey for a supermarket grab.[/dim]",
            "expensive": "[bold red]Expensive 💸[/bold red]\n[dim]Justifiable for high-end craft brew or imported specialty.[/dim]"
        },
        "wine": {
            "excellent": "[bold green]Excellent Deal 🏆[/bold green]\n[dim]Bargain bin pricing. If it tastes good, stock up![/dim]",
            "good": "[bold blue]Good Value 🍷[/bold blue]\n[dim]Great price for an everyday table wine.[/dim]",
            "average": "[bold yellow]Average 🤷[/bold yellow]\n[dim]Standard pricing. Good value if it's a premium vintage; slightly overpriced if it's bottom shelf.[/dim]",
            "expensive": "[bold red]Expensive 💸[/bold red]\n[dim]Premium pricing. This should be a fine wine or champagne.[/dim]"
        },
        "mid_strength": {
             "excellent": "[bold green]Excellent Deal 🏆[/bold green]\n[dim]Very cheap for liqueurs or fortified wines.[/dim]",
             "good": "[bold blue]Good Value 🍸[/bold blue]\n[dim]Solid price for standard liqueurs (e.g., Baileys) or sake.[/dim]",
             "average": "[bold yellow]Average 🤷[/bold yellow]\n[dim]Standard pricing. If this is a basic liqueur, it's fair. If it's premium port/sake, it's a good deal.[/dim]",
             "expensive": "[bold red]Expensive 💸[/bold red]\n[dim]You are paying a heavy premium for branding or importing here.[/dim]"
        },
        "spirit": {
             "excellent": "[bold green]Excellent Deal 🏆[/bold green]\n[dim]Extremely cheap. Ensure it's not rubbing alcohol![/dim]",
             "good": "[bold blue]Good Value 🥃[/bold blue]\n[dim]Great price for standard supermarket spirits.[/dim]",
             "average": "[bold yellow]Average 🤷[/bold yellow]\n[dim]Standard pricing for mid-shelf spirits. A bargain if it's a premium single malt![/dim]",
             "expensive": "[bold red]Expensive 💸[/bold red]\n[dim]Premium pricing territory. This should be top-shelf liquor.[/dim]"
        }
    }
    
    # Fallback to generic if the category isn't found
    cat_templates = templates.get(category, templates["generic"])
    
    # Return the specific verdict string
    return cat_templates.get(rating, f"Unknown rating: {rating}")