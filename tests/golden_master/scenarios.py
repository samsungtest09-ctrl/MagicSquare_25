"""GM-2 scenario SSOT — GM-TC-01~05 input grids."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final


@dataclass(frozen=True, slots=True)
class Scenario:
    """Single Golden Master scenario definition."""

    tc_id: str
    name: str
    grid: list[list[int]]


NORMAL_SUCCESS_GRID: Final[list[list[int]]] = [
    [16, 0, 2, 0],
    [5, 10, 11, 8],
    [9, 6, 7, 12],
    [4, 15, 14, 1],
]

REVERSE_SUCCESS_GRID: Final[list[list[int]]] = [
    [0, 0, 2, 13],
    [5, 10, 11, 8],
    [9, 6, 7, 12],
    [4, 15, 14, 1],
]

INVALID_BLANK_COUNT_GRID: Final[list[list[int]]] = [
    [1, 2, 3, 4],
    [5, 6, 7, 8],
    [9, 10, 11, 12],
    [13, 14, 15, 0],
]

DUPLICATE_NUMBER_GRID: Final[list[list[int]]] = [
    [1, 2, 0, 4],
    [5, 6, 7, 8],
    [9, 10, 8, 12],
    [13, 14, 15, 0],
]

NO_VALID_MAGIC_SQUARE_GRID: Final[list[list[int]]] = [
    [1, 2, 3, 4],
    [5, 6, 7, 8],
    [9, 10, 0, 12],
    [13, 14, 15, 0],
]

SCENARIOS: Final[tuple[Scenario, ...]] = (
    Scenario(tc_id="GM-TC-01", name="normal_success", grid=NORMAL_SUCCESS_GRID),
    Scenario(tc_id="GM-TC-02", name="reverse_success", grid=REVERSE_SUCCESS_GRID),
    Scenario(
        tc_id="GM-TC-03",
        name="invalid_blank_count",
        grid=INVALID_BLANK_COUNT_GRID,
    ),
    Scenario(tc_id="GM-TC-04", name="duplicate_number", grid=DUPLICATE_NUMBER_GRID),
    Scenario(
        tc_id="GM-TC-05",
        name="no_valid_magic_square",
        grid=NO_VALID_MAGIC_SQUARE_GRID,
    ),
)

SCENARIO_BY_TC_ID: Final[dict[str, Scenario]] = {
    scenario.tc_id: scenario for scenario in SCENARIOS
}
