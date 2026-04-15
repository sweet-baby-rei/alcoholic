<p align="center">
    <img src="assets/logo.webp" alt="Project Logo" width="520">
</p>

CLI calculator for alcohol value.

---

```bash
$ alcoholic 2.5 --beer
╭───────────────────────────────────────────────────────────────────────────╮
│  Receipt Summary:      0.50 L (inferred) @ 5.0% ABV (inferred) for $2.50  │
│  Pure Ethanol Volume:                                            0.025 L  │
│  Cost per Pure L:                                                 £80.00  │
│  Verdict:                                                     Good Price  │
│                                  Solid value for standard beer or cider.  │
╰───────────────────────────────────────────────────────────────────────────╯
```

```bash
$ alcoholic 14 --wine
╭───────────────────────────────────────────────────────────────────────────────────╮
│  Receipt Summary:            0.75 L (inferred) @ 12.0% ABV (inferred) for $14.00  │
│  Pure Ethanol Volume:                                                    0.090 L  │
│  Cost per Pure L:                                                        £155.56  │
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
Please drink responsibly. This is mathematical evaluation of ethanol volume, not a recommendation for your liver or your social life.
