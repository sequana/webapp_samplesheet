"""Shared pytest fixtures for app tests."""
import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).parent.parent
PACKAGE_DIR = PROJECT_ROOT / "check_my_sample_sheet"
sys.path.insert(0, str(PROJECT_ROOT))


@pytest.fixture
def app_path():
    """Path to the Streamlit app entrypoint."""
    return str(PACKAGE_DIR / "app.py")


@pytest.fixture
def examples_dir():
    """Path to the examples directory."""
    return PACKAGE_DIR / "examples"


@pytest.fixture
def valid_sample_sheet(examples_dir):
    """Content of a valid sample sheet."""
    return (examples_dir / "sample_sheet.csv").read_text()


@pytest.fixture
def invalid_sample_sheet(examples_dir):
    """Content of an invalid sample sheet (bad sample ID)."""
    return (examples_dir / "Bad_SampleSheet_alphanum.csv").read_text()
