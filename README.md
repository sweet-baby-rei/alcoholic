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

> A CLI tool to calculate the true *Bang for your Buck* of alcohol purchases. Evaluates the cost of pure ethanol across different currencies, volumes, and drink categories.

---

## 🚀 Installation

Because `alcoholic` is a standalone CLI tool, it's highly recommended to install it globally using `uv` (or `pipx`):

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

## ⚙️ Configuration

Use `alcoholic-config` to set your defaults:

```bash
# Set your default unit to pints and currency to GBP
alcoholic-config --unit pt --currency GBP

# View current setup
alcoholic-config
```

Your settings are safely tucked away in `~/.alcoholic.json`.

---

## ⚖️ Disclaimer
Please drink responsibly. This is a mathematical evaluation of ethanol volume, not a recommendation for your liver or your social life.
