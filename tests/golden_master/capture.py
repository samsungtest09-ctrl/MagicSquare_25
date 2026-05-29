"""Capture solver outcomes for Golden Master baseline generation."""

from __future__ import annotations

import copy
import io
import sys
from dataclasses import dataclass
from typing import Final, Literal

from golden_master.contracts import (
    find_blank_coords_row_major,
    find_missing_numbers_sorted,
)
from golden_master.scenarios import SCENARIOS, Scenario
from golden_master.serializer import serialize_all_scenario_blocks, serialize_scenario_block

MAGIC_CONSTANT: Final[int] = 34
GRID_SIZE: Final[int] = 4
EXPECTED_BLANK_COUNT: Final[int] = 2
MIN_VALUE: Final[int] = 1
MAX_VALUE: Final[int] = 16

AttemptKind = Literal["small_first", "reverse"]


class GoldenMasterCaptureError(Exception):
    """Raised when reference capture cannot classify a scenario outcome."""


@dataclass(frozen=True, slots=True)
class CaptureResult:
    """Structured API capture result for Golden Master tests."""

    scenario: Scenario
    success: bool
    payload: list[int] | None
    error: str | None
    attempt: AttemptKind | None
    serialized: str


def _count_blanks(grid: list[list[int]]) -> int:
    return sum(cell == 0 for row in grid for cell in row)


def _has_duplicate_nonzero(grid: list[list[int]]) -> bool:
    seen: set[int] = set()
    for row in grid:
        for value in row:
            if value == 0:
                continue
            if value in seen:
                return True
            seen.add(value)
    return False


def _is_magic_square(grid: list[list[int]]) -> bool:
    row_sums = [sum(row) for row in grid]
    col_sums = [
        sum(grid[row_index][col_index] for row_index in range(GRID_SIZE))
        for col_index in range(GRID_SIZE)
    ]
    main_diag = sum(grid[index][index] for index in range(GRID_SIZE))
    anti_diag = sum(grid[index][GRID_SIZE - 1 - index] for index in range(GRID_SIZE))
    sums = row_sums + col_sums + [main_diag, anti_diag]
    values = {value for row in grid for value in row}
    return all(total == MAGIC_CONSTANT for total in sums) and values == set(
        range(MIN_VALUE, MAX_VALUE + 1)
    )


def _solve_reference(grid: list[list[int]]) -> tuple[list[int], AttemptKind]:
    (row_one, col_one), (row_two, col_two) = find_blank_coords_row_major(grid)
    small, large = find_missing_numbers_sorted(grid)

    small_first = copy.deepcopy(grid)
    small_first[row_one - 1][col_one - 1] = small
    small_first[row_two - 1][col_two - 1] = large
    if _is_magic_square(small_first):
        return [row_one, col_one, small, row_two, col_two, large], "small_first"

    reverse = copy.deepcopy(grid)
    reverse[row_one - 1][col_one - 1] = large
    reverse[row_two - 1][col_two - 1] = small
    if _is_magic_square(reverse):
        return [row_one, col_one, large, row_two, col_two, small], "reverse"

    msg = "NO_VALID_MAGIC_SQUARE"
    raise GoldenMasterCaptureError(msg)


def _validate_reference(grid: list[list[int]]) -> str | None:
    blank_count = _count_blanks(grid)
    if blank_count != EXPECTED_BLANK_COUNT:
        return "INVALID_BLANK_COUNT"
    if _has_duplicate_nonzero(grid):
        return "DUPLICATE_NUMBER"
    return None


def capture_scenario_result(scenario: Scenario) -> CaptureResult:
    """Capture one scenario as a structured API result."""
    validation_error = _validate_reference(scenario.grid)
    if validation_error is not None:
        serialized = serialize_scenario_block(scenario, error=validation_error)
        return CaptureResult(
            scenario=scenario,
            success=False,
            payload=None,
            error=validation_error,
            attempt=None,
            serialized=serialized,
        )

    try:
        payload, attempt = _solve_reference(scenario.grid)
    except GoldenMasterCaptureError:
        serialized = serialize_scenario_block(scenario, error="NO_VALID_MAGIC_SQUARE")
        return CaptureResult(
            scenario=scenario,
            success=False,
            payload=None,
            error="NO_VALID_MAGIC_SQUARE",
            attempt=None,
            serialized=serialized,
        )

    serialized = serialize_scenario_block(scenario, output=payload)
    return CaptureResult(
        scenario=scenario,
        success=True,
        payload=payload,
        error=None,
        attempt=attempt,
        serialized=serialized,
    )


def capture_scenario(scenario: Scenario) -> str:
    """Capture one scenario outcome as a Golden Master text block."""
    return capture_scenario_result(scenario).serialized


def capture_scenario_stdout(scenario: Scenario) -> str:
    """Capture scenario output through stdout redirection."""
    buffer = io.StringIO()
    previous_stdout = sys.stdout
    sys.stdout = buffer
    try:
        result = capture_scenario_result(scenario)
        if result.success and result.payload is not None:
            print(result.serialized)
        elif result.error is not None:
            print(result.serialized)
    finally:
        sys.stdout = previous_stdout
    return buffer.getvalue()


def capture_all_scenarios() -> str:
    """Capture all GM scenarios into one expected file body."""
    blocks = [capture_scenario(scenario) for scenario in SCENARIOS]
    return serialize_all_scenario_blocks(blocks)
