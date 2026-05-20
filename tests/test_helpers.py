"""Unit tests for helper functions in app.py."""
import pytest

from app import load_example


def test_load_example_valid_returns_content():
    content = load_example("sample_sheet.csv")
    assert "[Header]" in content
    assert "[Data]" in content
    assert len(content) > 0


def test_load_example_settings():
    content = load_example("sample_sheet_settings_index.csv")
    assert "[Settings]" in content
    assert "[Data]" in content


def test_load_example_invalid():
    content = load_example("Bad_SampleSheet_alphanum.csv")
    assert "[Data]" in content


def test_load_example_missing_file_raises():
    with pytest.raises(FileNotFoundError):
        load_example("does_not_exist.csv")
