import os
import pytest
from vectorhawk.core.config import Config
from vectorhawk.core.logger import get_logger

logger = get_logger("test_config")


@pytest.fixture(autouse=True)
def setup_env_variables(monkeypatch):
    """Set up environment variables for testing."""
    monkeypatch.setenv("ES_HOST", "http://localhost:9200")
    monkeypatch.setenv("ES_USER", "test_user")
    monkeypatch.setenv("ES_PASSWORD", "test_password")
    monkeypatch.setenv("LLM_MODEL", "mistral-7b")
    monkeypatch.setenv("LLM_API_PORT", "8000")
    monkeypatch.setenv("DEBUG_MODE", "True")
    monkeypatch.setenv("LOG_LEVEL", "DEBUG")
    monkeypatch.setenv("LOG_DIR", "./logs")


def test_config_initialization():
    """Test that the configuration initializes correctly with valid env variables."""
    config = Config()  # Initialize the config
    assert config.ES_HOST == "http://localhost:9200"
    assert config.ES_USER == "test_user"
    assert config.ES_PASSWORD == "test_password"
    assert config.LLM_MODEL == "mistral-7b"
    assert config.LLM_API_PORT == 8000
    assert config.DEBUG_MODE is True
    assert config.LOG_LEVEL == "DEBUG"
    assert config.LOG_DIR == "./logs"


def test_missing_es_host():
    """Test that an exception is raised if ES_HOST is missing."""
    os.environ.pop("ES_HOST", None)  # Remove the environment variable
    with pytest.raises(
        ValueError, match="Elasticsearch host \\(ES_HOST\\) is not set."
    ):
        Config()  # This should raise an exception


def test_missing_es_password_with_user():
    """Test that an exception is raised if ES_USER is set without ES_PASSWORD."""
    os.environ["ES_PASSWORD"] = ""  # Set password to empty
    with pytest.raises(ValueError, match="ES_USER is set but ES_PASSWORD is missing."):
        Config()  # This should raise an exception


def test_invalid_llm_api_port():
    """Test that an exception is raised if LLM_API_PORT is not a valid integer."""
    os.environ["LLM_API_PORT"] = "not_a_number"  # Set invalid port
    with pytest.raises(ValueError):
        Config()  # This should raise an exception


@pytest.mark.parametrize("log_level", ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"])
def test_log_level_variations(log_level):
    """Test that various log levels are set correctly."""
    os.environ["LOG_LEVEL"] = log_level  # Set different log levels
    config = Config()  # Initialize the config
    assert config.LOG_LEVEL == log_level
