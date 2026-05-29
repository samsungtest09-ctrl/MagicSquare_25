"""Track A RED skeleton — U-OUT-01~02 (FR-05 output contract)."""

from __future__ import annotations

import pytest

from boundary.ui_boundary import UIBoundary


class TestUOut01SixElementArray:
    """U-OUT-01: valid solve returns int[6]."""

    def test_u_out_01_solve_valid_matrix_returns_six_element_array(self) -> None:
        """G1 valid input → payload length 6."""
        # Given: G1 matrix; Control mock execute → [2, 2, 7, 3, 3, 10]
        # ui = UIBoundary()
        # with patch("control.use_cases.solve_partial_magic_square.SolvePartialMagicSquare.execute") as mock_execute:
        #     mock_execute.return_value = [2, 2, 7, 3, 3, 10]
        #     matrix = grid_g1  # [[16,3,2,13],[5,0,11,8],[9,6,0,12],[4,15,14,1]]

        # When: UIBoundary.solve(matrix)

        # Then: len(payload) == 6 (GREEN)
        pytest.fail(
            "RED: U-OUT-01 — valid solve returns six-element int array"
        )


class TestUOut02OneIndexedCoords:
    """U-OUT-02: success payload coordinates are 1-indexed in 1..4."""

    def test_u_out_02_solve_success_coords_one_indexed_in_1_to_4(self) -> None:
        """G1 + mocked execute → r,c ∈ {1..4}."""
        # Given: G1; Control mock → [2, 2, 7, 3, 3, 10]
        # ui = UIBoundary()
        # with patch("...SolvePartialMagicSquare.execute") as mock_execute:
        #     mock_execute.return_value = [2, 2, 7, 3, 3, 10]

        # When: payload = UIBoundary.solve(matrix)

        # Then: payload[0], payload[1], payload[3], payload[4] in 1..4 (GREEN)
        pytest.fail(
            "RED: U-OUT-02 — success payload coordinates are 1-indexed (1..4)"
        )
