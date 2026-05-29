"""Shared pytest fixtures and constants for AC-FR-01-01 RED tests."""

from __future__ import annotations

from typing import Final

import pytest

# AC-FR-01-01 / PRD §8.1 INVALID_SIZE contract (README To-Do anchor)
AC_FR_01_01: Final[str] = "AC-FR-01-01"
INVALID_SIZE_CODE: Final[str] = "INVALID_SIZE"
INVALID_SIZE_MESSAGE: Final[str] = "Grid must be 4x4."

# Out-of-scope for this RED commit (AC-FR-01-02~05, FR-02~05)
OUT_OF_SCOPE_AC_IDS: Final[tuple[str, ...]] = (
    "AC-FR-01-02",
    "AC-FR-01-03",
    "AC-FR-01-04",
    "AC-FR-01-05",
)

OUT_OF_SCOPE_SAMPLE_GRIDS: Final[tuple[list[list[int]] | None, ...]] = (
    # Valid 4×4 with two blanks — Solver success path (FR-02~05)
    [
        [1, 2, 0, 4],
        [5, 6, 7, 8],
        [9, 10, 11, 12],
        [13, 14, 15, 16],
    ],
    # Blank count ≠ 2 (AC-FR-01-02 / ERR-BND-003)
    [
        [1, 2, 3, 4],
        [5, 6, 7, 8],
        [9, 10, 11, 12],
        [13, 14, 15, 0],
    ],
    # Value out of range (AC-FR-01-03 / ERR-BND-004)
    [
        [1, 2, 0, 4],
        [5, 6, 7, 17],
        [9, 10, 11, 12],
        [13, 14, 15, 0],
    ],
    # Duplicate non-zero (AC-FR-01-04 / ERR-BND-005)
    [
        [1, 2, 0, 4],
        [5, 6, 7, 8],
        [9, 10, 8, 12],
        [13, 14, 15, 0],
    ],
)


@pytest.fixture
def grid_none() -> None:
    """Explicit None grid for AC-FR-01-01 anchor."""
    return None


@pytest.fixture
def grid_empty_list() -> list[list[int]]:
    """Zero-row container."""
    return []


@pytest.fixture
def grid_four_rows_zero_cols() -> list[list[int]]:
    """Four rows with zero columns each."""
    return [[] for _ in range(4)]


@pytest.fixture
def grid_3x4() -> list[list[int]]:
    """Three rows, four columns — shape mismatch."""
    return [[0] * 4 for _ in range(3)]


@pytest.fixture
def grid_4x3() -> list[list[int]]:
    """Four rows, three columns — shape mismatch."""
    return [[0] * 3 for _ in range(4)]


@pytest.fixture
def grid_5x5() -> list[list[int]]:
    """Five rows, five columns — shape mismatch."""
    return [[0] * 5 for _ in range(5)]


# --- Report/09 G0~G3 SSOT placeholders (activate in GREEN) ---
# G0: [[16,3,2,13],[5,10,11,8],[9,6,7,12],[4,15,14,1]]
# G1: [[16,3,2,13],[5,0,11,8],[9,6,0,12],[4,15,14,1]]
# G2: [[0,14,15,4],[9,7,6,12],[5,11,10,8],[16,2,3,13]]  # D-SOL-02 TBD
# G3: [[1,2,3,4],[5,6,7,8],[9,10,0,12],[13,14,15,0]]
#
# @pytest.fixture
# def grid_g0() -> list[list[int]]:
#     ...
#
# @pytest.fixture
# def grid_g1() -> list[list[int]]:
#     ...
#
# @pytest.fixture
# def grid_g2() -> list[list[int]]:
#     ...
#
# @pytest.fixture
# def grid_g3() -> list[list[int]]:
#     ...
