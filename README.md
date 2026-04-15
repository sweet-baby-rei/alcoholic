# 🍺 Alcoholic CLI: The "Bang for your Buck" Optimizer

<img src="assets/logo.webp" alt="Project Logo" width="500">

Are you standing in a supermarket aisle, staring at a wall of liquids, trying to figure out if that "Value Vodka" is actually a better deal than the discounted case of Kopparberg? Stop doing mental math while sober—let your terminal do it for you.

`alcoholic` is a precision-engineered tool for the savvy consumer who wants to maximize their pure ethanol intake per unit of currency. It’s modern, it’s colorful, and it’s arguably over-engineered.

---

## 🚀 Installation

Since we use `hatchling` and `rich`, you're just a few keystrokes away from optimal efficiency:

```bash
git clone https://github.com/your-repo/alcoholic.git
cd alcoholic
pip install -e .
```

---

## ✨ Features

* **Smart Inference:** Don't know the ABV or volume? Just tell the app what you're buying (e.g., `--beer`, `--wine`, `--spirit`) and it will guess the industry standards for you.
* **Currency Savvy:** Supports USD, GBP, EUR, JPY, and IDR out of the box with live exchange rate fetching (and stale fallbacks for when the pub Wi-Fi is terrible).
* **Hybrid Input:** Supports power-user positional arguments OR explicit flags. Use `alcoholic 8 --wine` or `alcoholic --price 8 --wine`. It’s smart enough to figure it out.
* **Nuanced Verdicts:** Doesn't just give you a number; it tells you *why* that £8 bottle of wine is "Average" and whether you should justify it.
* **Beautiful UI:** Powered by `rich` for those crisp, colorful tables that make math feel like a party.

---

## 📖 Usage

### The "I'm in a Hurry" Mode
Just provide the price and a beverage type. The CLI infers the rest.
```bash
# Inferred: 0.75L @ 13% ABV
alcoholic 8 --wine

# Inferred: 0.7L @ 40% ABV
alcoholic 15 --vodka
```

### The "Precision" Mode
Provide the exact specs for that weird craft cider you found.
```bash
# Price, Quantity, and custom ABV
alcoholic 20 4.0 --cider --abv 7.0
```

### The "Global" Mode
Check the value while on holiday using local currency.
```bash
alcoholic 50000 --currency IDR --beer
```

---

## ⚙️ Configuration

Use the companion tool `alcoholic-config` to set your "home" defaults so you never have to type `--currency` again.

```bash
# Set your default unit to pints and currency to GBP
alcoholic-config --unit pt --currency GBP

# View current setup
alcoholic-config
```

Your settings are safely tucked away in `~/.alcoholic.json`.

---

## 🌍 Localized
Supports **English** and **Spanish**! Change your `language` key in the config file to see the app in "Valor por tu Dinero" mode.

---

## ⚖️ Disclaimer
This is a joke app. Please drink responsibly. The "Excellent Deal" rating is a mathematical evaluation of ethanol volume, not a recommendation for your liver or your social life.

*Developed with ❤️ (and potentially a pint of 7% "Vintage" cider).*