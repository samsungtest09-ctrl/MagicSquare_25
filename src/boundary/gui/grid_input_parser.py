"""Convert GUI cell text into a 4×4 integer grid for boundary validation."""

from __future__ import annotations

from boundary.constants import GRID_SIZE
from boundary.gui.constants import BLANK_CELL_VALUE, MAX_CELL_VALUE, MIN_CELL_VALUE


class GridInputParseError(Exception):
    """Raised when one or more GUI cells contain invalid values."""

    def __init__(self, message: str, row: int, col: int) -> None:
        """Store the user-facing message and the offending cell coordinates."""
        super().__init__(message)
        self.message = message
        self.row = row
        self.col = col


def format_cell_for_display(value: int) -> str:
    """Render a grid value for an entry widget (blank cells appear empty)."""
    if value == BLANK_CELL_VALUE:
        return ""
    return str(value)


def parse_cell_value(text: str, row: int, col: int) -> int:
    """Parse a single cell string into an integer grid value.

    Args:
        text: Raw entry widget text. Empty strings map to blank (0).
        row: 1-based row index for error messages.
        col: 1-based column index for error messages.

    Returns:
        Parsed integer in the allowed range.

    Raises:
        GridInputParseError: When the text is not a valid cell value.
    """
    stripped = text.strip()
    if stripped == "":
        return BLANK_CELL_VALUE
    try:
        value = int(stripped)
    except ValueError as exc:
        raise GridInputParseError(
            f"셀 ({row}, {col}): 숫자만 입력할 수 있습니다.",
            row=row,
            col=col,
        ) from exc
    if value < MIN_CELL_VALUE or value > MAX_CELL_VALUE:
        raise GridInputParseError(
            f"셀 ({row}, {col}): {MIN_CELL_VALUE}~{MAX_CELL_VALUE} 범위의 값만 "
            "입력할 수 있습니다.",
            row=row,
            col=col,
        )
    return value


def read_grid_from_cells(cells: list[list[str]]) -> list[list[int]]:
    """Build a 4×4 integer matrix from GUI entry values.

    Args:
        cells: Row-major cell text values from the UI.

    Returns:
        Parsed 4×4 grid suitable for boundary validation.

    Raises:
        GridInputParseError: When shape is wrong or any cell is invalid.
        ValueError: When the outer list is not 4×4.
    """
    if len(cells) != GRID_SIZE:
        raise ValueError(f"Expected {GRID_SIZE} rows, got {len(cells)}.")
    grid: list[list[int]] = []
    for row_index, row in enumerate(cells, start=1):
        if len(row) != GRID_SIZE:
            raise ValueError(
                f"Row {row_index} must contain {GRID_SIZE} cells, got {len(row)}."
            )
        parsed_row = [
            parse_cell_value(text, row_index, col_index)
            for col_index, text in enumerate(row, start=1)
        ]
        grid.append(parsed_row)
    return grid
