import json
import pytest
from unittest.mock import MagicMock
from typer.testing import CliRunner

from alcoholic.cli import calc_cli
from alcoholic.cli.calc_app import get_exchange_rate

runner = CliRunner()


@pytest.fixture(autouse=True)
def mock_config_file(tmp_path, monkeypatch):
    """Automatically mock the config file for ALL tests."""
    fake_config_file = tmp_path / ".alcoholic.json"
    monkeypatch.setattr("alcoholic.config.CONFIG_FILE", fake_config_file)
    return fake_config_file


# --- API / Exchange Rate Tests ---


def test_get_exchange_rate_usd():
    """USD immediately returns 1.0."""
    assert get_exchange_rate("USD", offline=False) == 1.0


def test_get_exchange_rate_offline():
    """Offline mode skips API and uses fallback dictionary."""
    # Assuming GBP fallback is 0.79
    assert get_exchange_rate("GBP", offline=True) == 0.79


def test_get_exchange_rate_online_success(mocker):
    """Test successful JSON parse from open.er-api.com."""
    mock_response = MagicMock()
    mock_response.read.return_value.decode.return_value = json.dumps(
        {"rates": {"CAD": 1.45}}
    )

    mock_context_manager = MagicMock()
    mock_context_manager.__enter__.return_value = mock_response

    mocker.patch("urllib.request.urlopen", return_value=mock_context_manager)

    assert get_exchange_rate("CAD", offline=False) == 1.45


def test_get_exchange_rate_online_failure(mocker):
    """Test API failure silently falls back to hardcoded rates."""
    mocker.patch("urllib.request.urlopen", side_effect=Exception("Network down"))
    # CAD fallback is 1.36
    assert get_exchange_rate("CAD", offline=False) == 1.36


# --- CLI Validation Tests ---


def test_calc_missing_price():
    """Test failure when no price is provided."""
    result = runner.invoke(calc_cli, ["--wine"])
    assert result.exit_code == 1
    assert "You must provide a price" in result.stdout


def test_calc_hybrid_positional_logic():
    """Test reconciling positionals vs flags."""
    # 1. Standard positionals: price=20, qty=0.5
    res1 = runner.invoke(calc_cli, ["20", "0.5", "--abv", "5"])
    assert res1.exit_code == 0

    # 2. Positional provided BUT --price flag is also used
    # The stray positional '0.5' should be dynamically assigned to quantity
    res2 = runner.invoke(calc_cli, ["0.5", "--price", "20", "--abv", "5"])
    assert res2.exit_code == 0
    assert "0.50 L" in res2.stdout


def test_calc_invalid_unit():
    """Test rejecting an unknown volume unit."""
    result = runner.invoke(calc_cli, ["20", "--wine", "--unit", "gallons"])
    assert result.exit_code == 1
    assert "Unknown volume unit" in result.stdout or "Error" in result.stdout


def test_calc_missing_quantity_or_abv():
    """Test failure when qty/abv are missing and no smart flag is used."""
    result = runner.invoke(calc_cli, ["20", "--abv", "5"])
    assert result.exit_code == 1
    assert "You must provide a Quantity and ABV" in result.stdout


def test_calc_zero_quantity():
    """Test failure when 0 or negative values are provided."""
    result = runner.invoke(calc_cli, ["20", "0", "--abv", "5"])
    assert result.exit_code == 1
    assert "Quantity and ABV must be greater than zero" in result.stdout


def test_calc_smart_drink_flags():
    """Test that all smart flags successfully infer their ABV and Qty."""
    flags = ["--beer", "--cider", "--wine", "--liqueur", "--spirit"]
    for flag in flags:
        res = runner.invoke(calc_cli, ["10", flag])
        assert res.exit_code == 0


# --- CLI Evaluation & Render Tests ---


def test_calc_threshold_ratings():
    """
    Test the four rating tiers: Excellent, Good, Average, Expensive.
    Using USD Beer/Cider (0.5L @ 5% = 0.025L Pure Ethanol)
    Cost per pure L thresholds: Exc < 75, Good < 100, Avg < 140
    """
    # Price $1.50 -> Cost per pure L = $60 (Excellent)
    res_exc = runner.invoke(calc_cli, ["1.50", "--beer", "-c", "USD"])
    assert "Excellent Deal" in res_exc.stdout

    # Price $2.00 -> Cost per pure L = $80 (Good)
    res_good = runner.invoke(calc_cli, ["2.00", "--beer", "-c", "USD"])
    assert "Good Price" in res_good.stdout

    # Price $3.00 -> Cost per pure L = $120 (Average)
    res_avg = runner.invoke(calc_cli, ["3.00", "--beer", "-c", "USD"])
    assert "Average" in res_avg.stdout

    # Price $4.00 -> Cost per pure L = $160 (Expensive)
    res_exp = runner.invoke(calc_cli, ["4.00", "--beer", "-c", "USD"])
    assert "Expensive" in res_exp.stdout


def test_calc_fallback_currency_logic(mocker):
    """
    Test using a currency not natively mapped in CURRENCY_THRESHOLDS.
    It should trigger API fallback and display the 'Evaluated against' dim text.
    """
    mocker.patch("urllib.request.urlopen", side_effect=Exception("Network error"))

    # CAD isn't natively supported, so it converts eval_cost to USD base
    result = runner.invoke(calc_cli, ["20", "0.75", "--abv", "12", "-c", "CAD"])
    assert result.exit_code == 0
    assert "Evaluated against:" in result.stdout
    assert "USD Base" in result.stdout
