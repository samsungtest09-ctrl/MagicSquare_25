"""Golden Master (GM-2) approval testing utilities."""

from golden_master.approve import (
    DEFAULT_EXPECTED_PATH,
    approve_golden_master,
    approve_scenario,
    approve_text,
    format_unified_diff,
)
from golden_master.capture import (
    CaptureResult,
    capture_all_scenarios,
    capture_scenario,
    capture_scenario_result,
    capture_scenario_stdout,
)
from golden_master.contracts import (
    assert_boundary_error_contract,
    assert_domain_error_contract,
    assert_one_index_coordinates,
    assert_reverse_fallback_combination,
    assert_row_major_blank_order,
    assert_six_element_int_array,
    assert_small_first_combination,
)
from golden_master.scenarios import SCENARIOS, SCENARIO_BY_TC_ID, Scenario

__all__ = [
    "CaptureResult",
    "DEFAULT_EXPECTED_PATH",
    "SCENARIOS",
    "SCENARIO_BY_TC_ID",
    "Scenario",
    "approve_golden_master",
    "approve_scenario",
    "approve_text",
    "assert_boundary_error_contract",
    "assert_domain_error_contract",
    "assert_one_index_coordinates",
    "assert_reverse_fallback_combination",
    "assert_row_major_blank_order",
    "assert_six_element_int_array",
    "assert_small_first_combination",
    "capture_all_scenarios",
    "capture_scenario",
    "capture_scenario_result",
    "capture_scenario_stdout",
    "format_unified_diff",
]
