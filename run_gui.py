"""Convenience launcher for the Magic Square XX GUI."""

from __future__ import annotations

import sys
from pathlib import Path

_SRC = Path(__file__).resolve().parent / "src"
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from boundary.gui.magic_square_app import run_app  # noqa: E402

if __name__ == "__main__":
    run_app()
