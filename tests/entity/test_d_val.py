"""Track B RED skeleton — D-VAL-01~06 (FR-04, I1~I5)."""

from __future__ import annotations

import pytest

from entity.services.magic_square_validator import is_magic_square


class TestDVal01CompleteGrid:
    """D-VAL-01: G0 complete grid → true."""

    def test_d_val_01_is_magic_square_g0_complete_grid_returns_true(self) -> None:
        """G0 is a valid complete 4×4 magic square."""
        # Given: G0 matrix
        # matrix = [[16,3,2,13],[5,10,11,8],[9,6,7,12],[4,15,14,1]]

        # When: is_magic_square(matrix)

        # Then: True (GREEN)
        pytest.fail(
            "RED: D-VAL-01 — G0 complete grid is_magic_square returns true"
        )


class TestDVal02RowSumMismatch:
    """D-VAL-02: row sum ≠ 34 → false."""

    def test_d_val_02_is_magic_square_row_sum_mismatch_returns_false(
        self,
    ) -> None:
        """G0 variant with one row sum not equal to M(34)."""
        # Given: G0-derived matrix with row sum mismatch
        # matrix = ...  # GREEN: mutate one row

        # When: is_magic_square(matrix)

        # Then: False (GREEN)
        pytest.fail(
            "RED: D-VAL-02 — row sum mismatch returns false"
        )


class TestDVal03ColSumMismatch:
    """D-VAL-03: column sum ≠ 34 → false."""

    def test_d_val_03_is_magic_square_col_sum_mismatch_returns_false(
        self,
    ) -> None:
        """G0 variant with one column sum not equal to M(34)."""
        # Given: G0-derived matrix with column sum mismatch

        # When: is_magic_square(matrix)

        # Then: False (GREEN)
        pytest.fail(
            "RED: D-VAL-03 — column sum mismatch returns false"
        )


class TestDVal04DiagonalMismatch:
    """D-VAL-04: diagonal sum ≠ 34 → false."""

    def test_d_val_04_is_magic_square_diagonal_mismatch_returns_false(
        self,
    ) -> None:
        """G0 variant with main or anti-diagonal sum ≠ M(34)."""
        # Given: G0-derived matrix with diagonal mismatch

        # When: is_magic_square(matrix)

        # Then: False (GREEN)
        pytest.fail(
            "RED: D-VAL-04 — diagonal sum mismatch returns false"
        )


class TestDVal05DuplicateOrOutOfRange:
    """D-VAL-05: 17 or duplicate in full grid → false."""

    def test_d_val_05_is_magic_square_duplicate_or_out_of_range_returns_false(
        self,
    ) -> None:
        """Full grid containing 17 or duplicate value → false."""
        # Given: 4×4 full grid with 17 or duplicate non-zero

        # When: is_magic_square(matrix)

        # Then: False (GREEN)
        pytest.fail(
            "RED: D-VAL-05 — duplicate or out-of-range full grid returns false"
        )


class TestDVal06ZeroInFullGrid:
    """D-VAL-06: zero in otherwise complete grid → false."""

    def test_d_val_06_is_magic_square_with_zero_in_full_grid_returns_false(
        self,
    ) -> None:
        """G0 with one cell replaced by 0 → false."""
        # Given: G0 + one 0 cell in full grid

        # When: is_magic_square(matrix)

        # Then: False (GREEN)
        pytest.fail(
            "RED: D-VAL-06 — zero in full grid returns false"
        )
