"""
    Unit tests: Loading configuration
"""

import json

import pytest

from load_functions import load_config

def test_load_config_normal():
    """Test loading a proper configuration file without errors."""
    load_config("tests/configs/config-test_normal.json")

def test_load_config_missing_file():
    """Test loading a configuration file that does not exist."""
    with pytest.raises(FileNotFoundError):
        load_config("tests/configs/config-test_missing.json")

def test_load_config_malformed_file():
    """Test loading a malformed configuration file."""
    with pytest.raises(json.JSONDecodeError):
        load_config("tests/configs/config-test_malformed.json")

def test_load_config_missing_options():
    """Test loading a configuration file that is missing required options."""
    with pytest.raises(Exception):
        load_config("tests/configs/config-test_missing_options.json")
