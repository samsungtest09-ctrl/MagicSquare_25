"""GUI-related named constants for the boundary layer."""

from typing import Final

from boundary.constants import GRID_SIZE

BLANK_CELL_VALUE: Final[int] = 0
MIN_CELL_VALUE: Final[int] = 0
MAX_CELL_VALUE: Final[int] = 16

APP_TITLE: Final[str] = "Magic Square XX — 4×4 마방진"
WINDOW_MIN_WIDTH: Final[int] = 480
WINDOW_MIN_HEIGHT: Final[int] = 520

__all__ = [
    "APP_TITLE",
    "BLANK_CELL_VALUE",
    "GRID_SIZE",
    "MAX_CELL_VALUE",
    "MIN_CELL_VALUE",
    "WINDOW_MIN_HEIGHT",
    "WINDOW_MIN_WIDTH",
]
