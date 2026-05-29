"""AC-FR-01-01: PRD §8.1 INVALID_SIZE — Boundary shape/null rejection (RED)."""

from __future__ import annotations

from typing import Any

import pytest
from pydantic import BaseModel

from boundary.validators.boundary_validator import BoundaryValidator
from tests.conftest import (
    AC_FR_01_01,
    INVALID_SIZE_CODE,
    INVALID_SIZE_MESSAGE,
    OUT_OF_SCOPE_AC_IDS,
    OUT_OF_SCOPE_SAMPLE_GRIDS,
)


class TestNormalFailureReturn:
    """AC-FR-01-01: PRD §8.1 INVALID_SIZE — Happy Path of Failure (failure result)."""

    def test_none_grid_returns_failure_result_not_success(
        self, grid_none: None
    ) -> None:
        """grid=None must yield a failure result object, not success."""
        # Given: explicit None grid (AC-FR-01-01 anchor)
        validator = BoundaryValidator()

        # When: Boundary validates the grid
        result = validator.validate(grid_none)

        # Then: outcome is a failure, not a success payload
        # AC-FR-01-01
        assert result.is_failure is True
        assert result.is_success is False

    def test_none_grid_returns_non_null_failure_object(
        self, grid_none: None
    ) -> None:
        """Failure path must return a concrete result object."""
        # Given: None grid
        validator = BoundaryValidator()

        # When: validate is invoked
        result = validator.validate(grid_none)

        # Then: caller receives a populated failure result
        # AC-FR-01-01
        assert result is not None

    def test_none_grid_failure_exposes_code_field(
        self, grid_none: None
    ) -> None:
        """Failure result exposes a machine-readable code field."""
        # Given: None grid
        validator = BoundaryValidator()

        # When: validate runs
        result = validator.validate(grid_none)

        # Then: code attribute exists for downstream mapping
        # AC-FR-01-01
        assert hasattr(result, "code")
        assert isinstance(result.code, str)

    def test_none_grid_failure_exposes_message_field(
        self, grid_none: None
    ) -> None:
        """Failure result exposes a human-readable message field."""
        # Given: None grid
        validator = BoundaryValidator()

        # When: validate runs
        result = validator.validate(grid_none)

        # Then: message attribute exists
        # AC-FR-01-01
        assert hasattr(result, "message")
        assert isinstance(result.message, str)

    def test_none_grid_does_not_return_solver_success_shape(
        self, grid_none: None
    ) -> None:
        """Invalid input must not masquerade as a six-int solver success."""
        # Given: None grid
        validator = BoundaryValidator()

        # When: validate runs
        result = validator.validate(grid_none)

        # Then: no success-only fields (e.g. six-int tuple) on failure path
        # AC-FR-01-01
        assert not hasattr(result, "values") or result.is_failure is True


class TestBoundaryValues:
    """AC-FR-01-01: PRD §8.1 INVALID_SIZE — shape/null edge grids."""

    def test_empty_list_grid_returns_failure_result(
        self, grid_empty_list: list[list[int]]
    ) -> None:
        """Empty list is rejected as invalid size."""
        # Given: grid=[]
        validator = BoundaryValidator()

        # When: validate is called
        result = validator.validate(grid_empty_list)

        # Then: failure result is returned
        # AC-FR-01-01
        assert result.is_failure is True
        assert result.code == INVALID_SIZE_CODE

    def test_four_empty_rows_grid_returns_failure_result(
        self, grid_four_rows_zero_cols: list[list[int]]
    ) -> None:
        """Four rows with zero columns each is not 4×4."""
        # Given: grid=[[]]*4 equivalent (fresh lists per row)
        validator = BoundaryValidator()

        # When: validate is called
        result = validator.validate(grid_four_rows_zero_cols)

        # Then: failure result is returned
        # AC-FR-01-01
        assert result.is_failure is True
        assert result.code == INVALID_SIZE_CODE

    def test_3x4_grid_returns_failure_result(self, grid_3x4: list[list[int]]) -> None:
        """3×4 matrix is rejected."""
        # Given: three rows, four columns
        validator = BoundaryValidator()

        # When: validate is called
        result = validator.validate(grid_3x4)

        # Then: failure result is returned
        # AC-FR-01-01
        assert result.is_failure is True
        assert result.code == INVALID_SIZE_CODE

    def test_4x3_grid_returns_failure_result(self, grid_4x3: list[list[int]]) -> None:
        """4×3 matrix is rejected."""
        # Given: four rows, three columns
        validator = BoundaryValidator()

        # When: validate is called
        result = validator.validate(grid_4x3)

        # Then: failure result is returned
        # AC-FR-01-01
        assert result.is_failure is True
        assert result.code == INVALID_SIZE_CODE

    def test_5x5_grid_returns_failure_result(self, grid_5x5: list[list[int]]) -> None:
        """5×5 matrix is rejected."""
        # Given: five rows, five columns
        validator = BoundaryValidator()

        # When: validate is called
        result = validator.validate(grid_5x5)

        # Then: failure result is returned
        # AC-FR-01-01
        assert result.is_failure is True
        assert result.code == INVALID_SIZE_CODE


class TestMessageExactMatch:
    """AC-FR-01-01: PRD §8.1 INVALID_SIZE — message string identity."""

    def test_none_grid_message_equals_prd_invalid_size_literal(
        self, grid_none: None
    ) -> None:
        """Message must match PRD §8.1 INVALID_SIZE text exactly."""
        # Given: None grid and PRD §8.1 reference string
        validator = BoundaryValidator()
        expected = INVALID_SIZE_MESSAGE

        # When: validate runs
        result = validator.validate(grid_none)

        # Then: character-level equality (no normalization)
        # AC-FR-01-01
        assert result.message == expected

    def test_none_grid_message_is_not_substring_match_only(
        self, grid_none: None
    ) -> None:
        """Message equality rejects partial/substring-only checks."""
        # Given: None grid
        validator = BoundaryValidator()

        # When: validate runs
        result = validator.validate(grid_none)

        # Then: full string match, not merely contained
        # AC-FR-01-01
        assert result.message == INVALID_SIZE_MESSAGE
        assert result.message != "Grid must be 4x4"

    def test_none_grid_message_length_matches_prd_literal(
        self, grid_none: None
    ) -> None:
        """Trailing punctuation in PRD §8.1 is part of the contract."""
        # Given: None grid
        validator = BoundaryValidator()

        # When: validate runs
        result = validator.validate(grid_none)

        # Then: length includes terminal period
        # AC-FR-01-01
        assert len(result.message) == len(INVALID_SIZE_MESSAGE)
        assert result.message.endswith(".")

    def test_shape_mismatch_grids_share_invalid_size_message(
        self, grid_3x4: list[list[int]]
    ) -> None:
        """Shape violations use the same PRD §8.1 message template."""
        # Given: 3×4 grid
        validator = BoundaryValidator()

        # When: validate runs
        result = validator.validate(grid_3x4)

        # Then: identical message to None anchor case
        # AC-FR-01-01
        assert result.message == INVALID_SIZE_MESSAGE

    def test_empty_list_message_equals_invalid_size_literal(
        self, grid_empty_list: list[list[int]]
    ) -> None:
        """Empty list uses the same PRD §8.1 message."""
        # Given: grid=[]
        validator = BoundaryValidator()

        # When: validate runs
        result = validator.validate(grid_empty_list)

        # Then: character-level message match
        # AC-FR-01-01
        assert result.message == INVALID_SIZE_MESSAGE


class TestInvalidSizeCode:
    """AC-FR-01-01: PRD §8.1 INVALID_SIZE — code field contract."""

    def test_none_grid_code_is_invalid_size_string(self, grid_none: None) -> None:
        """code must be exactly INVALID_SIZE."""
        # Given: None grid
        validator = BoundaryValidator()

        # When: validate runs
        result = validator.validate(grid_none)

        # Then: exact code string
        # AC-FR-01-01
        assert result.code == INVALID_SIZE_CODE

    def test_none_grid_code_is_not_err_bnd_prefix(self, grid_none: None) -> None:
        """AC scenario code INVALID_SIZE is distinct from ERR-BND-* storage."""
        # Given: None grid
        validator = BoundaryValidator()

        # When: validate runs
        result = validator.validate(grid_none)

        # Then: public code is INVALID_SIZE per §8.1
        # AC-FR-01-01
        assert result.code == "INVALID_SIZE"
        assert not result.code.startswith("ERR-BND-")

    @pytest.mark.parametrize(
        "grid_fixture",
        ["grid_empty_list", "grid_four_rows_zero_cols", "grid_3x4"],
    )
    def test_shape_edge_grids_code_is_invalid_size(
        self, grid_fixture: str, request: pytest.FixtureRequest
    ) -> None:
        """Parameterized shape edges all map to INVALID_SIZE."""
        # Given: in-scope invalid-shape grid fixture
        grid: Any = request.getfixturevalue(grid_fixture)
        validator = BoundaryValidator()

        # When: validate runs
        result = validator.validate(grid)

        # Then: INVALID_SIZE code
        # AC-FR-01-01
        assert result.code == INVALID_SIZE_CODE

    def test_invalid_size_code_length_is_twelve_chars(self, grid_none: None) -> None:
        """Guard against accidental code mutation or truncation."""
        # Given: None grid
        validator = BoundaryValidator()

        # When: validate runs
        result = validator.validate(grid_none)

        # Then: stable code token length
        # AC-FR-01-01
        assert len(result.code) == len(INVALID_SIZE_CODE)


class TestFailureResultStructure:
    """AC-FR-01-01: PRD §8.1 INVALID_SIZE — pydantic failure result shape."""

    def test_none_grid_result_is_validation_failure_model(
        self, grid_none: None
    ) -> None:
        """Return type is the designated failure result model."""
        # Given: None grid
        from boundary.models.validation_failure_result import (
            ValidationFailureResult,
        )

        validator = BoundaryValidator()

        # When: validate runs
        result = validator.validate(grid_none)

        # Then: pydantic failure DTO
        # AC-FR-01-01
        assert isinstance(result, ValidationFailureResult)

    def test_none_grid_result_is_pydantic_base_model(
        self, grid_none: None
    ) -> None:
        """Failure result participates in pydantic validation ecosystem."""
        # Given: None grid
        validator = BoundaryValidator()

        # When: validate runs
        result = validator.validate(grid_none)

        # Then: BaseModel subclass
        # AC-FR-01-01
        assert isinstance(result, BaseModel)

    def test_failure_result_model_declares_code_and_message_fields(
        self,
    ) -> None:
        """Schema exposes code and message for contract tests."""
        # Given: failure result model type
        from boundary.models.validation_failure_result import (
            ValidationFailureResult,
        )

        # When: inspecting model fields
        field_names = set(ValidationFailureResult.model_fields.keys())

        # Then: required contract fields exist
        # AC-FR-01-01
        assert "code" in field_names
        assert "message" in field_names

    def test_failure_result_model_declares_is_failure_flag(self) -> None:
        """Explicit is_failure flag distinguishes from success DTO."""
        # Given: failure result model type
        from boundary.models.validation_failure_result import (
            ValidationFailureResult,
        )

        # When: inspecting model fields
        field_names = set(ValidationFailureResult.model_fields.keys())

        # Then: failure discriminator present
        # AC-FR-01-01
        assert "is_failure" in field_names

    def test_none_grid_result_serializes_code_and_message(
        self, grid_none: None
    ) -> None:
        """Round-trip model_dump preserves contract fields."""
        # Given: None grid
        validator = BoundaryValidator()

        # When: validate and dump
        result = validator.validate(grid_none)
        payload = result.model_dump()

        # Then: serialized contract
        # AC-FR-01-01
        assert payload["code"] == INVALID_SIZE_CODE
        assert payload["message"] == INVALID_SIZE_MESSAGE
        assert payload["is_failure"] is True


class TestScopeRestriction:
    """AC-FR-01-01 only — AC-FR-01-02~05 and FR-02~05 cases excluded from this commit."""

    def test_out_of_scope_ac_ids_documented(self) -> None:
        """This RED commit targets AC-FR-01-01 only."""
        # Given: scope constants
        expected = ("AC-FR-01-02", "AC-FR-01-03", "AC-FR-01-04", "AC-FR-01-05")

        # When: comparing to module-level exclusion list
        # Then: FR-01 follow-on ACs are explicitly out of scope
        # AC-FR-01-01
        assert OUT_OF_SCOPE_AC_IDS == expected

    def test_out_of_scope_sample_grids_are_not_parametrized_here(self) -> None:
        """Valid solver / rule-violation grids are not in-scope fixtures."""
        # Given: documented exclusion samples
        assert len(OUT_OF_SCOPE_SAMPLE_GRIDS) >= 4

        # When: checking they represent non-shape-first failures
        # Then: at least one 4×4 grid present (shape-valid, rule-invalid)
        # AC-FR-01-01
        four_by_four = [g for g in OUT_OF_SCOPE_SAMPLE_GRIDS if g and len(g) == 4]
        assert len(four_by_four) >= 1

    def test_in_scope_grids_exclude_valid_two_blank_4x4(self) -> None:
        """TD-001 style success grids must not appear in AC-FR-01-01 tests."""
        # Given: first out-of-scope sample (valid 4×4, two blanks)
        valid_grid = OUT_OF_SCOPE_SAMPLE_GRIDS[0]
        assert valid_grid is not None

        # When: checking dimensions
        # Then: 4×4 — excluded from this module's Arrange tables
        # AC-FR-01-01
        assert len(valid_grid) == 4
        assert all(len(row) == 4 for row in valid_grid)

    def test_module_does_not_define_blank_count_violation_fixture(self) -> None:
        """AC-FR-01-02 blank-count cases belong to a later RED commit."""
        # Given: this test module's public fixtures from conftest only
        from tests import conftest

        # When: scanning conftest for a one-blank 4×4 fixture
        fixture_names = [name for name in dir(conftest) if name.startswith("grid_")]

        # Then: no dedicated blank-count violation fixture
        # AC-FR-01-01
        assert "grid_wrong_blank_count" not in fixture_names

    def test_module_does_not_define_duplicate_or_range_fixtures(self) -> None:
        """AC-FR-01-03~05 value rules are out of scope for this file."""
        # Given: conftest grid_* fixtures
        from tests import conftest

        fixture_names = [name for name in dir(conftest) if name.startswith("grid_")]

        # When: checking for FR-01 rule 3~5 fixtures
        # Then: only shape/null edge fixtures exist
        # AC-FR-01-01
        assert "grid_duplicate_eight" not in fixture_names
        assert "grid_cell_seventeen" not in fixture_names
