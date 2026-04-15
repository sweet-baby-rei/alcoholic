import json
import os
from pathlib import Path

from alcoholic.config.verdicts import get_verdict

CONFIG_FILE = Path.home() / ".alcoholic.json"
LOCALE_FILE = Path(__file__).parent / "locale.json"

LOCALES = json.loads(LOCALE_FILE.read_text())

# Base conversion rates to Litres
VOLUME_UNITS = {
    "L": 1.0,
    "ml": 0.001,
    "gal": 3.78541, # US Gallon
    "qt": 0.946353, # US Quart
    "pt": 0.473176, # US Pint
    "oz": 0.0295735 # US Fluid Ounce
}

DEFAULT_CONFIG = {
    "language": "en",
    "currency_symbol": "$",
    "default_unit": "L",
    "thresholds": {
        "excellent_under": 30,
        "good_under": 50,
        "average_under": 80
    }
}

FALLBACK_RATES = {
    "USD": 1.0,
    "EUR": 0.92,
    "GBP": 0.79,
    "JPY": 150.5,
    "IDR": 15500.0,
    "AUD": 1.53,
    "CAD": 1.36
}

# Native thresholds for specific currencies (Cost per pure Litre)
# Native thresholds for specific currencies (Cost per pure Litre)
# Native thresholds for specific currencies (Cost per pure Litre)
CURRENCY_THRESHOLDS = {
    "USD": {
        "symbol": "$",
        "generic":      {"excellent_under": 60, "good_under": 80, "average_under": 110},
        "spirit":       {"excellent_under": 50, "good_under": 65, "average_under": 90},
        "wine":         {"excellent_under": 70, "good_under": 90, "average_under": 120},
        "beer_cider":   {"excellent_under": 75, "good_under": 100, "average_under": 140},
        "mid_strength": {"excellent_under": 90, "good_under": 120, "average_under": 160}
    },
    "GBP": {
        "symbol": "£",
        "generic":      {"excellent_under": 55, "good_under": 75, "average_under": 100},
        "spirit":       {"excellent_under": 45, "good_under": 60, "average_under": 80},    
        "wine":         {"excellent_under": 65, "good_under": 75, "average_under": 105},    
        "beer_cider":   {"excellent_under": 60, "good_under": 85, "average_under": 130},   
        "mid_strength": {"excellent_under": 75, "good_under": 100, "average_under": 140}   
    },
    "EUR": {
        "symbol": "€",
        "generic":      {"excellent_under": 55, "good_under": 75, "average_under": 100},
        "spirit":       {"excellent_under": 45, "good_under": 60, "average_under": 80},
        "wine":         {"excellent_under": 60, "good_under": 80, "average_under": 110},
        "beer_cider":   {"excellent_under": 65, "good_under": 90, "average_under": 130},
        "mid_strength": {"excellent_under": 80, "good_under": 110, "average_under": 150}
    },
    "JPY": {
        "symbol": "¥",
        "generic":      {"excellent_under": 9000, "good_under": 12000, "average_under": 16000},
        "spirit":       {"excellent_under": 7500, "good_under": 10000, "average_under": 14000},
        "wine":         {"excellent_under": 10000, "good_under": 13000, "average_under": 18000},
        "beer_cider":   {"excellent_under": 12000, "good_under": 16000, "average_under": 22000},
        "mid_strength": {"excellent_under": 14000, "good_under": 18000, "average_under": 24000}
    },
    "IDR": {
        "symbol": "Rp",
        "generic":      {"excellent_under": 900000, "good_under": 1200000, "average_under": 1600000},
        "spirit":       {"excellent_under": 750000, "good_under": 1000000, "average_under": 1400000},
        "wine":         {"excellent_under": 1000000, "good_under": 1300000, "average_under": 1800000},
        "beer_cider":   {"excellent_under": 1200000, "good_under": 1600000, "average_under": 2200000},
        "mid_strength": {"excellent_under": 1400000, "good_under": 1800000, "average_under": 2400000}
    }
}

def load_config() -> dict:
    """Loads the user config, creating it with defaults if it doesn't exist."""
    if not CONFIG_FILE.exists():
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(DEFAULT_CONFIG, f, indent=4)
        return DEFAULT_CONFIG

    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            user_config = json.load(f)
            return {**DEFAULT_CONFIG, **user_config}

    except json.JSONDecodeError:
        return DEFAULT_CONFIG

def get_locale(lang: str) -> dict:
    """Returns the translation dictionary for the chosen language."""
    return LOCALES.get(lang, LOCALES["en"])


def save_config(new_config: dict):
    """Saves the updated configuration dictionary back to the JSON file."""
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(new_config, f, indent=4)