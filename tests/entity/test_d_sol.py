"""Track B RED skeleton — D-SOL-01~04 (FR-05, Control solution — Domain Mock 금지)."""

from __future__ import annotations

import pytest

from control.use_cases.solver import solution

# GREEN: from entity.exceptions import UnsolvableDomainError


class TestDSol01StepASmallFirst:
    """D-SOL-01: G1 Attempt1 small-first → [2,2,7,3,3,10]."""

    def test_d_sol_01_solution_g1_step_a_small_first_success(self) -> None:
        """G1 solution via small-first attempt (I8)."""
        # Given: G1 matrix
        # matrix = [[16,3,2,13],[5,0,11,8],[9,6,0,12],[4,15,14,1]]

        # When: solution(matrix)

        # Then: [2, 2, 7, 3, 3, 10] (GREEN)
        pytest.fail(
            "RED: D-SOL-01 — G1 Step A small-first success [2,2,7,3,3,10]"
        )


class TestDSol02StepBReverse:
    """D-SOL-02: G2 Step A fails, Step B reverse success."""

    def test_d_sol_02_solution_g2_step_a_fails_step_b_reverse_success(
        self,
    ) -> None:
        """G2 reverse attempt → [1,1,16,1,2,2] (I9)."""
        pytest.fail("RED: D-SOL-02 — G2 TBD")


class TestDSol03BothAttemptsFail:
    """D-SOL-03: G3 → UnsolvableDomainError."""

    def test_d_sol_03_solution_g3_both_attempts_fail_raises_unsolvable(
        self,
    ) -> None:
        """G3 raises UnsolvableDomainError (I10)."""
        # Given: G3 matrix
        # matrix = [[1,2,3,4],[5,6,7,8],[9,10,0,12],[13,14,15,0]]

        # When / Then: pytest.raises(UnsolvableDomainError) (GREEN)
        pytest.fail(
            "RED: D-SOL-03 — G3 both attempts fail raises UnsolvableDomainError"
        )


class TestDSol04ResultShape:
    """D-SOL-04: G1 success length 6 and 1-index coords."""

    def test_d_sol_04_solution_success_result_length_and_one_index_coords(
        self,
    ) -> None:
        """G1 solution len==6; coordinates in {1..4}."""
        # Given: G1 matrix

        # When: result = solution(matrix)

        # Then: len(result)==6; r,c in 1..4 (GREEN)
        pytest.fail(
            "RED: D-SOL-04 — success result length 6 and 1-index coords in 1..4"
        )
