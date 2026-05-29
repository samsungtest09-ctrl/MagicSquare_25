"""Golden Master contract assertions for solver output."""

from __future__ import annotations

from typing import Final, Literal

from golden_master.scenarios import Scenario

GRID_SIZE: Final[int] = 4
OUTPUT_LENGTH: Final[int] = 6
MIN_VALUE: Final[int] = 1
MAX_VALUE: Final[int] = 16
EXPECTED_BLANK_COUNT: Final[int] = 2

AttemptKind = Literal["small_first", "reverse"]

BOUNDARY_ERROR_CODES: Final[frozenset[str]] = frozenset(
    {"INVALID_BLANK_COUNT", "DUPLICATE_NUMBER"}
)
DOMAIN_ERROR_CODES: Final[frozenset[str]] = frozenset({"NO_VALID_MAGIC_SQUARE"})


def find_blank_coords_row_major(grid: list[list[int]]) -> tuple[tuple[int, int], tuple[int, int]]:
    """Return the first and second blank coordinates in row-major 1-index order."""
    blanks: list[tuple[int, int]] = []
    for row_index, row in enumerate(grid):
        for col_index, value in enumerate(row):
            if value == 0:
                blanks.append((row_index + 1, col_index + 1))
    first_blank, second_blank = blanks
    return first_blank, second_blank


def find_missing_numbers_sorted(grid: list[list[int]]) -> tuple[int, int]:
    """Return missing numbers in ascending order."""
    present = {value for row in grid for value in row if value != 0}
    missing = sorted(number for number in range(MIN_VALUE, MAX_VALUE + 1) if number not in present)
    small, large = missing
    return small, large


def assert_six_element_int_array(payload: list[int]) -> None:
    """Assert FR-05 success payload shape."""
    assert len(payload) == OUTPUT_LENGTH
    assert all(isinstance(value, int) for value in payload)


def assert_one_index_coordinates(payload: list[int]) -> None:
    """Assert coordinates are 1-indexed values in 1..4."""
    row_one, col_one, _, row_two, col_two, _ = payload
    for coordinate in (row_one, col_one, row_two, col_two):
        assert MIN_VALUE <= coordinate <= GRID_SIZE


def assert_row_major_blank_order(scenario: Scenario, payload: list[int]) -> None:
    """Assert payload blanks follow row-major discovery order."""
    (expected_row_one, expected_col_one), (expected_row_two, expected_col_two) = (
        find_blank_coords_row_major(scenario.grid)
    )
    row_one, col_one, _, row_two, col_two, _ = payload
    assert (row_one, col_one) == (expected_row_one, expected_col_one)
    assert (row_two, col_two) == (expected_row_two, expected_col_two)


def assert_small_first_combination(scenario: Scenario, payload: list[int]) -> None:
    """Assert Attempt 1 places the smaller missing number first."""
    small, large = find_missing_numbers_sorted(scenario.grid)
    _, _, number_one, _, _, number_two = payload
    assert number_one == small
    assert number_two == large


def assert_reverse_fallback_combination(scenario: Scenario, payload: list[int]) -> None:
    """Assert Attempt 2 places the larger missing number first."""
    small, large = find_missing_numbers_sorted(scenario.grid)
    _, _, number_one, _, _, number_two = payload
    assert number_one == large
    assert number_two == small


def assert_boundary_error_contract(error_code: str) -> None:
    """Assert boundary-layer Golden Master error codes."""
    assert error_code in BOUNDARY_ERROR_CODES


def assert_domain_error_contract(error_code: str) -> None:
    """Assert domain-layer Golden Master error codes."""
    assert error_code in DOMAIN_ERROR_CODES
