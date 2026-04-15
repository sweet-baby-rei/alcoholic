import json

from alcoholic.config import (
    load_config,
    save_config,
    get_locale,
    DEFAULT_CONFIG,
)
from alcoholic.config.verdicts import get_verdict


def test_load_config_creates_default(tmp_path, monkeypatch):
    """Test that load_config creates a default file if none exists."""
    # Create a fake path inside a temporary directory
    fake_config_file = tmp_path / ".alcoholic.json"
    # Overwrite the global CONFIG_FILE variable during this test
    monkeypatch.setattr("alcoholic.config.CONFIG_FILE", fake_config_file)

    assert not fake_config_file.exists()

    config = load_config()

    assert config == DEFAULT_CONFIG
    assert fake_config_file.exists()


def test_load_config_reads_existing(tmp_path, monkeypatch):
    """Test that load_config reads an existing valid JSON file."""
    fake_config_file = tmp_path / ".alcoholic.json"
    monkeypatch.setattr("alcoholic.config.CONFIG_FILE", fake_config_file)

    # Create a fake config file with custom data
    custom_config = {**DEFAULT_CONFIG, "language": "es"}
    fake_config_file.write_text(json.dumps(custom_config), encoding="utf-8")

    config = load_config()

    assert config["language"] == "es"


def test_load_config_handles_corrupt_json(tmp_path, monkeypatch):
    """Test that load_config falls back to default if JSON is corrupt."""
    fake_config_file = tmp_path / ".alcoholic.json"
    monkeypatch.setattr("alcoholic.config.CONFIG_FILE", fake_config_file)

    fake_config_file.write_text("{corrupt_json: true", encoding="utf-8")

    config = load_config()

    assert config == DEFAULT_CONFIG


def test_save_config(tmp_path, monkeypatch):
    """Test that save_config correctly writes to the filesystem."""
    fake_config_file = tmp_path / ".alcoholic.json"
    monkeypatch.setattr("alcoholic.config.CONFIG_FILE", fake_config_file)

    custom_config = {**DEFAULT_CONFIG, "default_unit": "pt"}
    save_config(custom_config)

    assert fake_config_file.exists()
    saved_data = json.loads(fake_config_file.read_text(encoding="utf-8"))
    assert saved_data["default_unit"] == "pt"


def test_get_locale():
    """Test that locales load correctly."""
    en_locale = get_locale("en")
    assert en_locale["verdict"] == "Verdict:"

    es_locale = get_locale("es")
    assert es_locale["verdict"] == "Veredicto:"

    # Fallback to English for unknown locales
    unknown_locale = get_locale("fr")
    assert unknown_locale["verdict"] == "Verdict:"


def test_get_verdict():
    """Test that the verdict logic maps correctly."""
    # Test a known category and rating
    verdict = get_verdict("beer_cider", "excellent")
    assert "Excellent Deal" in verdict

    # Test fallback to generic if category isn't explicitly defined
    generic_verdict = get_verdict("unknown_category", "good")
    assert "Good Price" in generic_verdict

    # Test unknown rating fallback
    unknown_rating = get_verdict("wine", "terrible")
    assert "Unknown rating: terrible" in unknown_rating
