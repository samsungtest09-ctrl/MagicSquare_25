"""Track A RED skeleton — U-IN-04 (FR-01-AC-03, E004 value range)."""

from __future__ import annotations

import pytest

from boundary.input_validator import InputValidator


class TestUIn04ValueRange:
    """U-IN-04: Cell values must be 0 or 1..16."""

    def test_u_in_04_negative_value_returns_e004(self) -> None:
        """-1 in 4×4 matrix → E004 failure envelope."""
        # Given: 4×4 matrix containing -1
        # validator = InputValidator()
        # matrix = [[1, 2, 0, 4], [5, 6, 7, -1], [9, 10, 11, 12], [13, 14, 15, 0]]

        # When: InputValidator.validate(matrix)

        # Then: code E004; message exact (GREEN)
        pytest.fail(
            "RED: U-IN-04 — value out of range (-1) returns E004 failure envelope"
        )

    def test_u_in_04_seventeen_returns_e004(self) -> None:
        """17 in 4×4 matrix → E004 failure envelope."""
        # Given: 4×4 matrix containing 17
        # validator = InputValidator()
        # matrix = [[1, 2, 0, 4], [5, 6, 7, 17], [9, 10, 11, 12], [13, 14, 15, 0]]

        # When: InputValidator.validate(matrix)

        # Then: code E004; message exact (GREEN)
        pytest.fail(
            "RED: U-IN-04 — value out of range (17) returns E004 failure envelope"
        )
