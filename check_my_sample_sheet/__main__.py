"""Console entry point: launch the Streamlit sample sheet validator.

Installed as the ``check-my-sample-sheet`` command (see pyproject.toml). Any
extra arguments are forwarded to ``streamlit run`` (e.g. ``--server.port``).
"""
import sys
from pathlib import Path

from streamlit.web import cli as stcli


def main():
    app = str(Path(__file__).resolve().parent / "app.py")
    sys.argv = ["streamlit", "run", app, *sys.argv[1:]]
    sys.exit(stcli.main())


if __name__ == "__main__":
    main()
