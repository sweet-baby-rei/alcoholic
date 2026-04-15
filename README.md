<p align="center">
    <img src="assets/logo.webp" alt="Project Logo" width="520">
</p>

<p align="center">
    <img src="https://img.shields.io/badge/Python-3.9_%7C_3.10_%7C_3.11_%7C_3.12_%7C_3.13_%7C_3.14-blue.svg" alt="Python Versions">
</p>
<p align="center">
    <a href="https://github.com/sweet-baby-rei/alcoholic/actions">
        <img src="https://github.com/sweet-baby-rei/alcoholic/actions/workflows/ci.yml/badge.svg" alt="Tests">
    </a>
    <a href="https://codecov.io/gh/sweet-baby-rei/alcoholic">
        <img src="https://codecov.io/gh/sweet-baby-rei/alcoholic/graph/badge.svg" alt="codecov">
    </a>
    <a href="https://github.com/astral-sh/ruff">
        <img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json" alt="Ruff">
    </a>
</p>

> A CLI tool to calculate the *Bang for your Buck* of alcohol purchases. Evaluates the cost of pure ethanol across different currencies, volumes, and drink categories.

---

## 🚀 Installation

`alcoholic` is available on PyPI:

```
pip install alcoholic
```

As `alcoholic` is a standalone CLI tool, you may want to install it globally using **[uv](https://docs.astral.sh/uv/)** or **[pipx](https://pipx.pypa.io/stable/)**:

```bash
uv tool install alcoholic
```

---

## 💻 Usage

```text
$ alcoholic 2.5 --beer
╭───────────────────────────────────────────────────────────────────────────╮
│  Receipt Summary:      0.50 L (inferred) @ 5.0% ABV (inferred) for $2.50  │
│  Pure Ethanol Volume:                                            0.025 L  │
│  Cost per Pure L:                                                 £80.00  │
│  Verdict:                                                     Good Price  │
│                                  Solid value for standard beer or cider.  │
╰───────────────────────────────────────────────────────────────────────────╯
```

```text
$ alcoholic --price 17 --abv 13.5 --wine
╭───────────────────────────────────────────────────────────────────────────────────╮
│  Receipt Summary:                       0.75 L (inferred) @ 13.5% ABV for £17.00  │
│  Pure Ethanol Volume:                                                    0.101 L  │
│  Cost per Pure L:                                                        £167.90  │
│  Verdict:                                                              Expensive  │
│                        Premium pricing. This should be a fine wine or champagne.  │
╰───────────────────────────────────────────────────────────────────────────────────╯
```

```text
$ alcoholic --help

 Usage: alcoholic [OPTIONS] [PRICE] [QUANTITY]

 Calculates the cost per pure unit of ethanol.

╭─ Arguments ───────────────────────────────────────────────────────────────────────────────────╮
│   pos_price         [PRICE]     Total price (Positional)                                      │
│   pos_quantity      [QUANTITY]  Volume quantity (Positional)                                  │
╰───────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ─────────────────────────────────────────────────────────────────────────────────────╮
│ --price                           -p      FLOAT  Total price (Flag)                           │
│ --quantity                        -q      FLOAT  Volume quantity (Flag)                       │
│ --abv                             -a      FLOAT  Alcohol percentage (e.g., 13.5)              │
│ --unit                            -u      TEXT   Override default volume unit                 │
│ --currency                        -c      TEXT   Currency code (e.g., USD, JPY, GBP)          │
│ --offline                                        Skip live API conversion                     │
│ --beer                                           Evaluate as Beer (Defaults 5% ABV, 0.5L)     │
│ --cider                                          Evaluate as Cider (Defaults 5% ABV, 0.5L)    │
│ --wine                                           Evaluate as Wine (Defaults 13% ABV, 0.75L)   │
│ --liqueur,--sake,--soju,--port                   Evaluate as Liqueur (Defaults 20% ABV, 0.7L) │
│ --spirit,--vodka,--rum,--whiskey  -s             Evaluate as Spirit (Defaults 40% ABV, 0.7L)  │
│ --install-completion                             Install completion for the current shell.    │
│ --show-completion                                Show completion for the current shell, to    │
│                                                  copy it or customize the installation.       │
│ --help                                           Show this message and exit.                  │
╰───────────────────────────────────────────────────────────────────────────────────────────────╯
```

## ⚙️ Configuration

Use `alcoholic-config` to set your defaults:

```bash
# Set your default unit to pints and currency to GBP
alcoholic-config --unit pt --currency GBP

# View current setup
alcoholic-config
```

Settings are saved to `~/.alcoholic.json`.

---

## ⚖️ Disclaimer
Please drink responsibly. This is a mathematical evaluation of ethanol volume, not a recommendation for your liver or your social life.
