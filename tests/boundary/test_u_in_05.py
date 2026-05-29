"""Track A RED skeleton — U-IN-05 (FR-01-AC-04, E005 duplicate non-zero)."""

from __future__ import annotations

import pytest

from boundary.input_validator import InputValidator


class TestUIn05DuplicateNonZero:
    """U-IN-05: Non-zero values must be unique."""

    def test_u_in_05_duplicate_nonzero_returns_e005(self) -> None:
        """non-zero 8 duplicated with exactly two blanks → E005."""
        # Given: 4×4, two zeros, non-zero 8 appears twice
        # validator = InputValidator()
        # matrix = [[1, 2, 0, 4], [5, 6, 7, 8], [9, 10, 8, 12], [13, 14, 15, 0]]

        # When: InputValidator.validate(matrix)

        # Then: code E005; message exact (GREEN)
        pytest.fail(
            "RED: U-IN-05 — duplicate non-zero returns E005 failure envelope"
        )
