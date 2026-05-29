"""Track A RED skeleton — U-FLOW-02 extended (FR-01-AC-05, execute 0회)."""

from __future__ import annotations

import pytest

from boundary.ui_boundary import UIBoundary


class TestUFlow02InvalidNeverCallsExecute:
    """U-FLOW-02: invalid input must not invoke SolvePartialMagicSquare.execute."""

    def test_u_flow_02_null_never_calls_execute(self) -> None:
        """matrix=null → execute call_count 0."""
        # Given: matrix = None
        # ui = UIBoundary()
        # with patch("control.use_cases.solve_partial_magic_square.SolvePartialMagicSquare.execute") as spy:

        # When: UIBoundary.solve(matrix)

        # Then: spy.call_count == 0 (GREEN)
        pytest.fail(
            "RED: U-FLOW-02 — null input never calls SolvePartialMagicSquare.execute"
        )

    def test_u_flow_02_empty_list_never_calls_execute(self) -> None:
        """matrix=[] → execute call_count 0."""
        # Given: matrix = []
        # ui = UIBoundary()
        # with patch("...SolvePartialMagicSquare.execute") as spy:

        # When: UIBoundary.solve(matrix)

        # Then: spy.call_count == 0 (GREEN)
        pytest.fail(
            "RED: U-FLOW-02 — empty list never calls SolvePartialMagicSquare.execute"
        )

    def test_u_flow_02_g0_zero_blanks_never_calls_execute(self) -> None:
        """G0 (0 blanks) → execute call_count 0."""
        # Given: G0 complete grid (Report/09 §3)
        # matrix = [[16,3,2,13],[5,10,11,8],[9,6,7,12],[4,15,14,1]]
        # with patch("...SolvePartialMagicSquare.execute") as spy:

        # When: UIBoundary.solve(matrix)

        # Then: spy.call_count == 0 (GREEN)
        pytest.fail(
            "RED: U-FLOW-02 — G0 zero-blank grid never calls execute"
        )

    def test_u_flow_02_out_of_range_never_calls_execute(self) -> None:
        """value range violation → execute call_count 0."""
        # Given: 4×4 with 17
        # matrix = [[1,2,0,4],[5,6,7,17],[9,10,11,12],[13,14,15,0]]
        # with patch("...SolvePartialMagicSquare.execute") as spy:

        # When: UIBoundary.solve(matrix)

        # Then: spy.call_count == 0 (GREEN)
        pytest.fail(
            "RED: U-FLOW-02 — out-of-range grid never calls execute"
        )

    def test_u_flow_02_duplicate_nonzero_never_calls_execute(self) -> None:
        """duplicate non-zero → execute call_count 0."""
        # Given: 4×4, duplicate 8, two blanks
        # matrix = [[1,2,0,4],[5,6,7,8],[9,10,8,12],[13,14,15,0]]
        # with patch("...SolvePartialMagicSquare.execute") as spy:

        # When: UIBoundary.solve(matrix)

        # Then: spy.call_count == 0 (GREEN)
        pytest.fail(
            "RED: U-FLOW-02 — duplicate non-zero grid never calls execute"
        )
