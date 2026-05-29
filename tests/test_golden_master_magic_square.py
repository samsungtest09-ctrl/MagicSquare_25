"""GM-2 Golden Master regression tests for Magic Square Solver output.

[TAG][GoldenMaster]
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

_TESTS_DIR = Path(__file__).resolve().parent
if str(_TESTS_DIR) not in sys.path:
    sys.path.insert(0, str(_TESTS_DIR))

from golden_master.approve import DEFAULT_EXPECTED_PATH, approve_golden_master, approve_scenario
from golden_master.capture import capture_all_scenarios, capture_scenario_result, capture_scenario_stdout
from golden_master.contracts import (
    assert_boundary_error_contract,
    assert_domain_error_contract,
    assert_one_index_coordinates,
    assert_reverse_fallback_combination,
    assert_row_major_blank_order,
    assert_six_element_int_array,
    assert_small_first_combination,
)
from golden_master.scenarios import SCENARIO_BY_TC_ID

pytestmark = pytest.mark.golden_master


class TestGoldenMasterMagicSquareBaseline:
    """[TAG][GoldenMaster] Full-file approval baseline."""

    def test_golden_master_file_matches_expected_baseline(self) -> None:
        """Compare open(expected).read() against the captured full baseline body."""
        actual = capture_all_scenarios()
        expected_path = DEFAULT_EXPECTED_PATH
        approved = approve_golden_master(expected_path)
        assert approved == actual
        assert expected_path.read_text(encoding="utf-8") == actual


@pytest.mark.golden_master
class TestGoldenMasterMagicSquareTc01NormalSuccess:
    """GM-TC-01: 정상 조합 성공 (small-first)."""

    def test_gm_tc_01_normal_combination_success(self) -> None:
        """[GM-TC-01] small-first success matches the approved baseline block."""
        scenario = SCENARIO_BY_TC_ID["GM-TC-01"]
        api_result = capture_scenario_result(scenario)
        stdout_result = capture_scenario_stdout(scenario)

        approve_scenario(scenario)
        assert api_result.success is True
        assert api_result.attempt == "small_first"
        assert api_result.payload is not None
        assert_six_element_int_array(api_result.payload)
        assert_one_index_coordinates(api_result.payload)
        assert_row_major_blank_order(scenario, api_result.payload)
        assert_small_first_combination(scenario, api_result.payload)
        assert stdout_result.strip() == api_result.serialized.strip()


@pytest.mark.golden_master
class TestGoldenMasterMagicSquareTc02ReverseSuccess:
    """GM-TC-02: reverse 조합 성공."""

    def test_gm_tc_02_reverse_combination_success(self) -> None:
        """[GM-TC-02] reverse fallback success matches the approved baseline block."""
        scenario = SCENARIO_BY_TC_ID["GM-TC-02"]
        api_result = capture_scenario_result(scenario)
        stdout_result = capture_scenario_stdout(scenario)

        approve_scenario(scenario)
        assert api_result.success is True
        assert api_result.attempt == "reverse"
        assert api_result.payload is not None
        assert_six_element_int_array(api_result.payload)
        assert_one_index_coordinates(api_result.payload)
        assert_row_major_blank_order(scenario, api_result.payload)
        assert_reverse_fallback_combination(scenario, api_result.payload)
        assert stdout_result.strip() == api_result.serialized.strip()


@pytest.mark.golden_master
class TestGoldenMasterMagicSquareTc03InvalidBlankCount:
    """GM-TC-03: INVALID_BLANK_COUNT."""

    def test_gm_tc_03_invalid_blank_count_error_contract(self) -> None:
        """[GM-TC-03] blank-count violation matches the approved error block."""
        scenario = SCENARIO_BY_TC_ID["GM-TC-03"]
        api_result = capture_scenario_result(scenario)

        approve_scenario(scenario)
        assert api_result.success is False
        assert api_result.error == "INVALID_BLANK_COUNT"
        assert_boundary_error_contract(api_result.error)


@pytest.mark.golden_master
class TestGoldenMasterMagicSquareTc04DuplicateNumber:
    """GM-TC-04: DUPLICATE_NUMBER."""

    def test_gm_tc_04_duplicate_number_error_contract(self) -> None:
        """[GM-TC-04] duplicate non-zero violation matches the approved error block."""
        scenario = SCENARIO_BY_TC_ID["GM-TC-04"]
        api_result = capture_scenario_result(scenario)

        approve_scenario(scenario)
        assert api_result.success is False
        assert api_result.error == "DUPLICATE_NUMBER"
        assert_boundary_error_contract(api_result.error)


@pytest.mark.golden_master
class TestGoldenMasterMagicSquareTc05NoValidMagicSquare:
    """GM-TC-05: NO_VALID_MAGIC_SQUARE."""

    def test_gm_tc_05_no_valid_magic_square_error_contract(self) -> None:
        """[GM-TC-05] both attempts fail with the approved domain error block."""
        scenario = SCENARIO_BY_TC_ID["GM-TC-05"]
        api_result = capture_scenario_result(scenario)

        approve_scenario(scenario)
        assert api_result.success is False
        assert api_result.error == "NO_VALID_MAGIC_SQUARE"
        assert_domain_error_contract(api_result.error)
