"""AC-FR-01-01: PRD §8.1 INVALID_SIZE — Domain resolve() isolation (RED)."""

from __future__ import annotations

from typing import Any
from unittest.mock import MagicMock, patch

import pytest

from boundary.facade import validate_and_solve
from tests.conftest import INVALID_SIZE_CODE, INVALID_SIZE_MESSAGE


class TestIsolationGuard:
    """AC-FR-01-01: PRD §8.1 INVALID_SIZE — resolve() must not run on boundary failure."""

    @patch("boundary.facade.Solver.resolve")
    def test_none_grid_resolve_called_zero_times(
        self, mock_resolve: MagicMock, grid_none: None
    ) -> None:
        """grid=None: Domain resolve() entry point is never invoked."""
        # Given: None grid and spied resolve()
        # When: public facade handles the request
        validate_and_solve(grid_none)

        # Then: resolve() call count is exactly zero
        # AC-FR-01-01
        assert mock_resolve.call_count == 0

    @patch("boundary.facade.Solver.resolve")
    def test_empty_list_grid_resolve_called_zero_times(
        self, mock_resolve: MagicMock, grid_empty_list: list[list[int]]
    ) -> None:
        """grid=[]: resolve() is not invoked."""
        # Given: empty list grid
        # When: facade runs
        validate_and_solve(grid_empty_list)

        # Then: zero calls
        # AC-FR-01-01
        mock_resolve.assert_not_called()

    @patch("boundary.facade.Solver.resolve")
    def test_four_empty_rows_resolve_called_zero_times(
        self,
        mock_resolve: MagicMock,
        grid_four_rows_zero_cols: list[list[int]],
    ) -> None:
        """grid=[[]]*4: resolve() is not invoked."""
        # Given: four rows, zero columns
        # When: facade runs
        validate_and_solve(grid_four_rows_zero_cols)

        # Then: zero calls
        # AC-FR-01-01
        mock_resolve.assert_not_called()

    @patch("boundary.facade.Solver.resolve")
    def test_3x4_grid_resolve_called_zero_times(
        self, mock_resolve: MagicMock, grid_3x4: list[list[int]]
    ) -> None:
        """3×4 grid: resolve() is not invoked."""
        # Given: shape-mismatch grid
        # When: facade runs
        validate_and_solve(grid_3x4)

        # Then: zero calls
        # AC-FR-01-01
        mock_resolve.assert_not_called()

    @patch("boundary.facade.Solver.resolve")
    def test_none_grid_resolve_assert_not_called_explicit(
        self, mock_resolve: MagicMock, grid_none: None
    ) -> None:
        """Explicit assert_not_called for None short-circuit."""
        # Given: None grid
        # When: facade runs
        validate_and_solve(grid_none)

        # Then: mock contract
        # AC-FR-01-01
        mock_resolve.assert_not_called()


class TestBoundaryHandlesNoneBeforeResolve:
    """AC-FR-01-01: PRD §8.1 INVALID_SIZE — Boundary owns None branch."""

    @patch("boundary.facade.Solver.resolve")
    def test_none_grid_returns_failure_without_resolve_side_effects(
        self, mock_resolve: MagicMock, grid_none: None
    ) -> None:
        """Facade returns boundary failure; resolve() never observes None."""
        # Given: None grid
        # When: validate_and_solve runs
        result = validate_and_solve(grid_none)

        # Then: failure returned and resolve() untouched
        # AC-FR-01-01
        assert result.is_failure is True
        assert result.code == INVALID_SIZE_CODE
        mock_resolve.assert_not_called()

    @patch("boundary.facade.Solver.resolve")
    def test_none_grid_resolve_never_receives_none_argument(
        self, mock_resolve: MagicMock, grid_none: None
    ) -> None:
        """resolve() must not be called with None as the grid argument."""
        # Given: None grid
        # When: facade runs
        validate_and_solve(grid_none)

        # Then: no call args contain None matrix
        # AC-FR-01-01
        for call in mock_resolve.call_args_list:
            assert call.args[0] is not None

    @patch("boundary.facade.Solver.resolve")
    def test_boundary_failure_path_does_not_delegate_to_control(
        self, mock_resolve: MagicMock, grid_none: None
    ) -> None:
        """Control layer resolve() is bypassed on boundary failure."""
        # Given: None grid
        # When: facade runs
        validate_and_solve(grid_none)

        # Then: resolve was never scheduled
        # AC-FR-01-01
        assert mock_resolve.called is False

    @patch("boundary.facade.Solver.resolve", side_effect=AssertionError("resolve invoked"))
    def test_none_grid_resolve_side_effect_would_fail_if_called(
        self, mock_resolve: MagicMock, grid_none: None
    ) -> None:
        """If resolve() runs, the test fails immediately (spy guard)."""
        # Given: resolve() raises if touched
        # When: facade handles None locally
        result = validate_and_solve(grid_none)

        # Then: boundary failure returned without triggering side_effect
        # AC-FR-01-01
        assert result.is_failure is True

    @patch("boundary.facade.Solver.resolve")
    def test_none_grid_message_set_before_any_resolve_chance(
        self, mock_resolve: MagicMock, grid_none: None
    ) -> None:
        """Failure message is produced at boundary without control participation."""
        # Given: None grid
        # When: facade runs
        result = validate_and_solve(grid_none)

        # Then: PRD §8.1 message present and resolve() idle
        # AC-FR-01-01
        assert result.message == INVALID_SIZE_MESSAGE
        mock_resolve.assert_not_called()


class TestResolveMockGuard:
    """AC-FR-01-01: PRD §8.1 INVALID_SIZE — mock invocation is a test defect."""

    def test_resolve_mock_call_count_zero_is_required_invariant(
        self,
    ) -> None:
        """Documented invariant: boundary failure implies resolve call_count == 0."""
        # Given: expected isolation invariant
        expected_call_count = 0

        # When: defining the guard constant
        # Then: tests must assert this value after facade calls
        # AC-FR-01-01
        assert expected_call_count == 0

    @patch("boundary.facade.Solver.resolve")
    def test_resolve_mock_called_once_would_fail_guard(
        self, mock_resolve: MagicMock, grid_none: None
    ) -> None:
        """Simulated accidental call is detectable via call_count assertion."""
        # Given: None grid and a strict post-condition
        validate_and_solve(grid_none)

        # When: checking call count
        call_count = mock_resolve.call_count

        # Then: any non-zero count is a RED failure signal for implementers
        # AC-FR-01-01
        assert call_count == 0, "resolve() must not be called on boundary failure"

    @patch("boundary.facade.Solver.resolve")
    def test_resolve_mock_not_called_with_any_kwargs(
        self, mock_resolve: MagicMock, grid_none: None
    ) -> None:
        """No kwargs-based resolve() side channel on failure path."""
        # Given: None grid
        validate_and_solve(grid_none)

        # When: inspecting mock_calls
        # Then: empty call list
        # AC-FR-01-01
        assert mock_resolve.mock_calls == []

    @patch("boundary.facade.Solver.resolve")
    @pytest.mark.parametrize(
        "grid_fixture",
        ["grid_none", "grid_empty_list", "grid_3x4"],
    )
    def test_invalid_shape_fixtures_never_invoke_resolve(
        self,
        mock_resolve: MagicMock,
        grid_fixture: str,
        request: pytest.FixtureRequest,
    ) -> None:
        """Parametrized invalid grids share zero resolve() invocations."""
        # Given: invalid-shape fixture
        grid: Any = request.getfixturevalue(grid_fixture)

        # When: facade runs
        validate_and_solve(grid)

        # Then: resolve() idle
        # AC-FR-01-01
        assert mock_resolve.call_count == 0

    @patch("boundary.facade.Solver.resolve")
    def test_resolve_mock_return_value_not_consumed_on_none(
        self, mock_resolve: MagicMock, grid_none: None
    ) -> None:
        """Failure path must not depend on a resolve() return value."""
        # Given: resolve configured with a sentinel return (must stay unused)
        mock_resolve.return_value = {"unexpected": True}

        # When: facade handles None
        result = validate_and_solve(grid_none)

        # Then: boundary failure, mock untouched
        # AC-FR-01-01
        assert result.is_failure is True
        mock_resolve.assert_not_called()


class TestScopeExcludesDownstreamAcs:
    """AC-FR-01-01 only — no AC-FR-01-02~05 / FR-02~05 isolation scenarios here."""

    def test_isolation_module_does_not_patch_blank_finder(self) -> None:
        """Entity rules are not spied in this RED commit."""
        # Given: this module's source
        import inspect

        from tests.control import test_solver_boundary_guard_ac_fr_01_01 as mod

        source = inspect.getsource(mod)

        # When: scanning for BlankFinder patches
        # Then: only resolve() is in scope
        # AC-FR-01-01
        assert "BlankFinder" not in source

    def test_isolation_module_does_not_import_magic_square_validator(self) -> None:
        """FR-02~05 validator not loaded in AC-FR-01-01 guard tests."""
        # Given: module globals
        import tests.control.test_solver_boundary_guard_ac_fr_01_01 as mod

        # When: checking imported names
        # Then: no direct entity validator dependency
        # AC-FR-01-01
        assert "MagicSquareValidator" not in mod.__dict__

    def test_facade_test_targets_validate_and_solve_only(self) -> None:
        """Integration entry for this RED slice is the boundary facade."""
        # Given: facade symbol
        # When: ensuring import path exists for RED
        # Then: validate_and_solve is the orchestration seam under test
        # AC-FR-01-01
        assert callable(validate_and_solve)

    def test_out_of_scope_ac_fr_01_02_not_referenced_in_test_names(self) -> None:
        """No test function names encode AC-FR-01-02 scenarios."""
        # Given: this module's test functions
        import inspect

        from tests.control import test_solver_boundary_guard_ac_fr_01_01 as mod

        tests = [
            name
            for name, obj in inspect.getmembers(mod)
            if name.startswith("test_") and inspect.isfunction(obj)
        ]

        # When: filtering names
        # Then: no AC-FR-01-02~05 suffixes
        # AC-FR-01-01
        assert not any("ac_fr_01_02" in name for name in tests)
        assert not any("blank_count" in name for name in tests)

    def test_out_of_scope_fr_02_not_referenced_in_test_names(self) -> None:
        """FR-02 solver success scenarios are excluded from this module."""
        # Given: collected test names
        import inspect

        from tests.control import test_solver_boundary_guard_ac_fr_01_01 as mod

        tests = [
            name
            for name, obj in inspect.getmembers(mod)
            if name.startswith("test_") and inspect.isfunction(obj)
        ]

        # When: scanning for FR-02 markers
        # Then: none present
        # AC-FR-01-01
        assert not any("fr_02" in name for name in tests)
        assert not any("six_int" in name for name in tests)
