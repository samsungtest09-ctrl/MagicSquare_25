"""Tests for boundary GUI grid input parsing."""

from __future__ import annotations

import pytest

from boundary.gui.grid_input_parser import (
    GridInputParseError,
    format_cell_for_display,
    parse_cell_value,
    read_grid_from_cells,
)


class TestFormatCellForDisplay:
    """Display formatting for entry widgets."""

    def test_blank_cell_renders_empty_string(self) -> None:
        assert format_cell_for_display(0) == ""

    def test_nonzero_renders_decimal_string(self) -> None:
        assert format_cell_for_display(7) == "7"


class TestParseCellValue:
    """Single-cell parsing rules."""

    def test_empty_string_maps_to_blank(self) -> None:
        assert parse_cell_value("", 1, 1) == 0

    def test_whitespace_maps_to_blank(self) -> None:
        assert parse_cell_value("   ", 2, 3) == 0

    def test_valid_integer_in_range(self) -> None:
        assert parse_cell_value("16", 4, 4) == 16

    def test_non_numeric_raises_with_coordinates(self) -> None:
        with pytest.raises(GridInputParseError) as exc_info:
            parse_cell_value("ab", 2, 1)
        assert exc_info.value.row == 2
        assert exc_info.value.col == 1

    def test_out_of_range_raises(self) -> None:
        with pytest.raises(GridInputParseError):
            parse_cell_value("17", 1, 2)


class TestReadGridFromCells:
    """Full grid assembly from GUI cells."""

    def test_reads_4x4_grid(self) -> None:
        cells = [
            ["16", "3", "2", "13"],
            ["5", "", "11", "8"],
            ["9", "6", "", "12"],
            ["4", "15", "14", "1"],
        ]
        grid = read_grid_from_cells(cells)
        assert grid == [
            [16, 3, 2, 13],
            [5, 0, 11, 8],
            [9, 6, 0, 12],
            [4, 15, 14, 1],
        ]

    def test_rejects_wrong_row_count(self) -> None:
        with pytest.raises(ValueError):
            read_grid_from_cells([["1", "2", "3", "4"]] * 3)
