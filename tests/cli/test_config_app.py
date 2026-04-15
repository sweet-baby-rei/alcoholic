import json
import pytest
from typer.testing import CliRunner

from alcoholic.cli import config_cli

# Create a single runner to use across all tests
runner = CliRunner()


@pytest.fixture(autouse=True)
def mock_config_file(tmp_path, monkeypatch):
    """Automatically mock the config file for ALL tests in this file."""
    fake_config_file = tmp_path / ".alcoholic.json"
    monkeypatch.setattr("alcoholic.config.CONFIG_FILE", fake_config_file)
    return fake_config_file


def test_config_view_defaults():
    """Test viewing the config when no arguments are passed."""
    # Simulates running `alcoholic-config` with no flags
    result = runner.invoke(config_cli)

    assert result.exit_code == 0
    assert "Current Configuration:" in result.stdout
    assert "Currency: USD" in result.stdout
    assert "Unit:     L" in result.stdout


def test_config_update_currency(mock_config_file):
    """Test updating the currency saves correctly and converts to uppercase."""
    # Simulates running `alcoholic-config --currency gbp`
    result = runner.invoke(config_cli, ["--currency", "gbp"])

    assert result.exit_code == 0
    assert "Default currency updated to: GBP" in result.stdout

    # Verify it actually saved to our fake filesystem
    saved_data = json.loads(mock_config_file.read_text(encoding="utf-8"))
    assert saved_data["active_currency"] == "GBP"


def test_config_update_unit(mock_config_file):
    """Test updating the volume unit saves correctly."""
    # Simulates running `alcoholic-config --unit ml`
    result = runner.invoke(config_cli, ["--unit", "ml"])

    assert result.exit_code == 0
    assert "Default volume unit updated to: ml" in result.stdout

    # Verify it actually saved
    saved_data = json.loads(mock_config_file.read_text(encoding="utf-8"))
    assert saved_data["default_unit"] == "ml"


def test_config_invalid_unit():
    """Test that providing an invalid unit throws an error and exits."""
    # Simulates running `alcoholic-config --unit gallons`
    result = runner.invoke(config_cli, ["--unit", "gallons"])

    # Exit code 1 indicates a failure/error occurred
    assert result.exit_code == 1
    assert "Error:" in result.stdout
    assert "Unknown unit 'gallons'" in result.stdout


def test_config_update_both(mock_config_file):
    """Test updating both currency and unit at the same time."""
    # Simulates running `alcoholic-config -c JPY -u pt`
    result = runner.invoke(config_cli, ["-c", "JPY", "-u", "pt"])

    assert result.exit_code == 0

    saved_data = json.loads(mock_config_file.read_text(encoding="utf-8"))
    assert saved_data["active_currency"] == "JPY"
    assert saved_data["default_unit"] == "pt"
