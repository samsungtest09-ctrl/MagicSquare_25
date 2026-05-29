"""Track B RED skeleton — D-MIS-01 (FR-03, I7/I11 missing numbers sorted)."""

from __future__ import annotations

import pytest

from entity.services.missing_number_finder import find_not_exist_nums


class TestDMis01MissingNumbers:
    """D-MIS-01: G1 → (7, 10) sorted — Domain Mock 금지."""

    def test_d_mis_01_find_not_exist_nums_g1_returns_7_and_10_sorted(
        self,
    ) -> None:
        """G1 missing numbers 7 and 10 in ascending order."""
        # Given: G1 matrix
        # matrix = [[16,3,2,13],[5,0,11,8],[9,6,0,12],[4,15,14,1]]

        # When: find_not_exist_nums(matrix)

        # Then: (7, 10) (GREEN)
        pytest.fail(
            "RED: D-MIS-01 — G1 missing numbers (7, 10) sorted ascending"
        )
