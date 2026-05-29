"""Track B RED skeleton — D-LOC-01 (FR-02, I6 row-major blanks 1-index)."""

from __future__ import annotations

import pytest

from entity.services.blank_finder import find_blank_coords


class TestDLoc01BlankCoords:
    """D-LOC-01: G1 → (2,2,3,3) row-major 1-index — Domain Mock 금지."""

    def test_d_loc_01_find_blank_coords_g1_row_major_one_index(self) -> None:
        """G1 blanks at (2,2) and (3,3) in 1-index coordinates."""
        # Given: G1 matrix
        # matrix = [[16,3,2,13],[5,0,11,8],[9,6,0,12],[4,15,14,1]]

        # When: find_blank_coords(matrix)

        # Then: (2, 2, 3, 3) (GREEN)
        pytest.fail(
            "RED: D-LOC-01 — G1 row-major blank coords (2,2,3,3) 1-index"
        )
