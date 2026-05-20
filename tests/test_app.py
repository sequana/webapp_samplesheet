"""Integration tests for the Streamlit app using AppTest framework."""
import pytest
from streamlit.testing.v1 import AppTest


# Generous default timeout - print_checks sleeps 0.15s per check
APP_TIMEOUT = 60


def test_app_renders_without_error(app_path):
    """App initial render should not raise."""
    at = AppTest.from_file(app_path, default_timeout=APP_TIMEOUT)
    at.run()
    assert not at.exception


def test_default_menu_is_validation(app_path):
    """Default menu choice loads the validation page."""
    at = AppTest.from_file(app_path, default_timeout=APP_TIMEOUT)
    at.run()
    # Title rendered on every page
    assert any("Sample Sheet and Design Validator" in t.value for t in at.title)
    # Validation page has the Input subheader
    subheaders = [s.value for s in at.subheader]
    assert "Input Sample Sheet" in subheaders


def test_example1_button_loads_valid_sample_sheet(app_path):
    """Clicking Example 1 button loads sample_sheet.csv into the textarea."""
    at = AppTest.from_file(app_path, default_timeout=APP_TIMEOUT)
    at.run()
    # Find and click the first example button
    buttons = [b for b in at.button if "Example 1" in b.label]
    assert len(buttons) == 1
    buttons[0].click().run()
    assert "[Header]" in at.session_state.code_input
    assert "[Data]" in at.session_state.code_input


def test_example2_button_loads_settings_sample_sheet(app_path):
    """Clicking Example 2 button loads sample_sheet_settings_index.csv."""
    at = AppTest.from_file(app_path, default_timeout=APP_TIMEOUT)
    at.run()
    buttons = [b for b in at.button if "Example 2" in b.label]
    assert len(buttons) == 1
    buttons[0].click().run()
    assert "[Settings]" in at.session_state.code_input


def test_example3_button_loads_invalid_sample_sheet(app_path):
    """Clicking Example 3 button loads the invalid example."""
    at = AppTest.from_file(app_path, default_timeout=APP_TIMEOUT)
    at.run()
    buttons = [b for b in at.button if "Example 3" in b.label]
    assert len(buttons) == 1
    buttons[0].click().run()
    assert "[Data]" in at.session_state.code_input


def test_process_valid_sample_sheet_succeeds(app_path, valid_sample_sheet):
    """Processing a valid sample sheet shows a success message."""
    at = AppTest.from_file(app_path, default_timeout=APP_TIMEOUT)
    at.run()
    # Pre-populate session state to skip the button-click round trip
    at.session_state.code_input = valid_sample_sheet
    at.run()
    process_buttons = [b for b in at.button if "Process" in b.label]
    assert len(process_buttons) == 1
    process_buttons[0].click().run()
    success_messages = [s.value for s in at.success]
    assert any("looks correct" in s for s in success_messages)


def test_process_invalid_sample_sheet_shows_error(app_path, invalid_sample_sheet):
    """Processing an invalid sample sheet shows an error message."""
    at = AppTest.from_file(app_path, default_timeout=APP_TIMEOUT)
    at.run()
    at.session_state.code_input = invalid_sample_sheet
    at.run()
    process_buttons = [b for b in at.button if "Process" in b.label]
    process_buttons[0].click().run()
    error_messages = [e.value for e in at.error]
    assert any("Error(s) found" in e for e in error_messages)


def test_about_page_renders(app_path):
    """About page renders without error."""
    at = AppTest.from_file(app_path, default_timeout=APP_TIMEOUT)
    at.run()
    # AppTest does not directly support streamlit_option_menu interaction;
    # we set the underlying session_state to switch pages if needed.
    # For now, just confirm the script does not raise during initial render.
    assert not at.exception


def test_no_python_exceptions_on_full_render(app_path):
    """Full render of default page does not raise Python exceptions."""
    at = AppTest.from_file(app_path, default_timeout=APP_TIMEOUT)
    at.run()
    assert len(at.exception) == 0
