# 결함 목록 (Defect List)

| 항목 | 내용 |
|---|---|
| **기준 문서** | `docs/test_plan.md` (TP-MS-4X4-FR01), README RED To-Do |
| **스냅샷 일자** | 2026-05-29 |
| **pytest 스냅샷** | 57 passed, **1 failed** (`python -m pytest -q`) |

> **상태**: *Open* = 미해결 · *Resolved* = 수정·검증 완료

---

## 결함 테이블

| ID | Severity | AC ID | 재현 절차 | 기대값 | 실제값 | 근본 원인 | 수정 요약 |
|---|---|---|---|---|---|---|---|
| DEF-001 | Critical | AC-FR-01-01 | RED 단계에서 `python -m pytest tests/boundary tests/control` 실행 (구현·`src` 패키지 없음) | 테스트 수집·실행 성공 | `ModuleNotFoundError: No module named 'boundary'` (또는 `control`) | `boundary` / `control` 패키지 및 `pytest` import 경로 미구성 | `src/boundary`, `src/control` 스켈레톤 추가; `pytest.ini`에 `pythonpath = src` 설정 (**Resolved**) |
| DEF-002 | Critical | AC-FR-01-01 | `grid=None` 입력 → `BoundaryValidator.validate()` 또는 `validate_and_solve(None)` | `code="INVALID_SIZE"`, `message="Grid must be 4x4."` | `TypeError` (`len(None)`) 또는 Domain으로 `None` 전파 (가드 없을 때) | `grid is None` 선행 분기 누락 | `_has_invalid_shape()`에 `grid is None` 조건 추가; 실패 DTO 반환 (**Resolved**) |
| DEF-003 | Low | AC-FR-01-01 | `pytest …::test_isolation_module_does_not_patch_blank_finder` | 모듈에 `BlankFinder` 패치·임포트 없음 | `AssertionError` (assert·주석에 `BlankFinder` 자기 참조) | `inspect.getsource` 전체 문자열 금지 검사 | AST/`patch` 대상만 검사하거나 금지 토큰을 assertion 밖으로 분리 (**Open**) |
| DEF-004 | Info | AC-FR-01-01 | 유효 4×4 `grid`로 `validate_and_solve(grid)` 호출 | AC-FR-01-01 범위 외(별도 TP) | `NotImplementedError` | P0는 null·형상 거부만 포함 | FR-02+에서 `Solver.resolve()` 구현 (의도된 skeleton 한계) |

---

## AC-FR-01-01 회귀 요약 (2026-05-29)

| 구분 | 결과 |
|---|---|
| Track A — Boundary (`tests/boundary/`) | **31/31 통과** |
| Track B — Control 격리 (`tests/control/`, DEF-003 제외) | **20/21 통과** |
| Entity (`tests/entity/`) | **4/4 통과** |
| **미해결 Open** | DEF-003 (테스트 설계 결함, 제품 로직 무관) |

---

## 추적

| Test Case | 결함 ID |
|---|---|
| TC-BND-001 / TC-A-01~07 | DEF-001, DEF-002 (Resolved) |
| TC-B-04 (범위 제한 메타 검증) | DEF-003 (Open) |

---

*다음 QA 액션: DEF-003 수정 후 전체 `pytest` GREEN 확인 → README 「모든 결함 수정 후 회귀 테스트 통과 확인」 체크.*
