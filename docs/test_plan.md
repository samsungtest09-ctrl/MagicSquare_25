# Magic Square 4×4 — 테스트 계획서 (Test Plan)

| 항목 | 내용 |
|---|---|
| **문서 ID** | TP-MS-4X4-FR01 |
| **기준 샘플** | **AC-FR-01-01**: `grid=None` → `INVALID_SIZE` |
| **대응 PRD** | SC-BND-001 → `ERR-BND-001` (`BoundaryValidationError`) |
| **스택** | Python 3.10+, pytest, pydantic (입력 DTO·계약), `unittest.mock` |
| **아키텍처** | ECB — `boundary` → `control` → `entity` |
| **TDD** | Dual-Track (Track A: Boundary / Track B: Domain) |
| **작성일** | 2026-05-29 |

---

## 1. 목적 및 범위

### 1.1 목적

- **FR-01 Input Verification (Boundary)** 를 pytest 단위·통합 테스트로 고정한다.
- 샘플 AC **AC-FR-01-01**(`grid=None` → `INVALID_SIZE`)을 **RED 테스트의 첫 앵커**로 삼고, 동일 검증 규칙 체인에 속한 형상·null 경계를 확장한다.
- Boundary 검증 실패 시 **Domain 해 결정 진입점(Control `Solver` / `SolveUseCase`)이 호출되지 않음**을 mock/spy로 검증한다.

### 1.2 In-Scope (본 계획서)

| 구분 | 포함 |
|---|---|
| 입력 형상·null | `None`, `[]`, `[[]]*4`, 3×4 / 4×3 / 5×5 |
| 오류 매핑 | `INVALID_SIZE` 및 PRD `ERR-BND-001`~`002` |
| ECB 격리 | Boundary 실패 → Control/Entity 미호출 |
| 커버리지 | Domain ≥ 95%, Boundary ≥ 85% (NFR-01/02) |

### 1.3 Out-of-Scope (본 계획서에서 테스트 설계 제외)

| 항목 | 사유 |
|---|---|
| **4×4 정상 입력** (유효 2빈칸 행렬, TD-001 등) | AC-FR-01-01(입력 거부) 범위 외 — Solver 성공·FR-02~05는 별도 Test Plan / Track B·Integration에서 다룸 |
| 16칸 완전 채움 PASS/FAIL 검증기 (Report/01) | PRD Out-of-Scope (별도 Epic) |
| UI·DB·Web·N×N 일반화 | PRD Out-of-Scope |

### 1.4 용어·오류 코드 매핑

| 테스트 계획 (AC/결과) | PRD 오류 코드 | 메시지 템플릿 (참고) |
|---|---|---|
| `INVALID_SIZE` (null·형상 위반 통칭) | `ERR-BND-001` | `Input matrix must not be null` |
| `INVALID_SIZE` (행·열 수 불일치) | `ERR-BND-002` | `Matrix must be 4x4` |

> 구현 시 예외 타입은 `BoundaryValidationError(error_code, message)` 로 통일한다. 테스트 assertion은 **`error_code`** 를 1차 기준으로, AC 명칭 `INVALID_SIZE` 는 시나리오 ID·파라미터화 키로 사용한다.

---

## 2. pytest 단위 테스트 범위 및 우선순위

### 2.1 레이어별 테스트 대상

| 레이어 | 모듈(예정) | 단위 테스트 초점 | 우선순위 |
|---|---|---|---|
| **Boundary** | `boundary.validators.boundary_validator` | FR-01 규칙 1~2 (null, 4×4 형상), 오류 코드·메시지 | **P0** |
| **Control** | `control.use_cases.solver` | Boundary 통과 후에만 Entity 규칙·Attempt 오케스트레이션 | P1 (본 계획: mock 대상) |
| **Entity** | `entity.rules.*` | BlankFinder, MissingNumberFinder, MagicSquareValidator | P2 (본 계획: 직접 호출 금지 시나리오만 간접 검증) |

### 2.2 우선순위 정의

| 우선순위 | 범위 | RED 시작 순서 | 완료 기준 |
|---|---|---|---|
| **P0** | AC-FR-01-01, 빈 리스트, `[[]]*4`, 3×4/4×3/5×5, Solver 미호출 | 1 | 해당 테스트 GREEN + Boundary 라인 커버리지 ≥ 85% (형상 검증 분기) |
| **P1** | FR-01 규칙 3~5 (빈칸 개수, 값 범위, 중복) — SC-BND-003~005 | 2 | ERR-BND-003~005 + Solver 미호출 |
| **P2** | Boundary 출력 계약 (길이 6, 1-index) — SC-BND-006~007 | 3 | 성공 경로 전용 (별도 TP) |
| **P3** | Integration (CLI/파사드 → Boundary → Control) | 4 | E2E 오류 전파 |

### 2.3 권장 테스트 디렉터리

```
tests/
├── boundary/
│   ├── test_boundary_validator_fr01.py    # P0: AC-FR-01-01, 형상 경계
│   └── test_boundary_validator_fr01_rules.py  # P1: 빈칸·범위·중복
├── control/
│   └── test_solver_boundary_guard.py      # mock: Domain 진입 차단
└── entity/
    └── ...                                 # Track B (본 계획 Out-of-Scope 항목 제외)
```

### 2.4 pytest 관례

- **AAA** (Arrange–Act–Assert) 패턴 고정.
- 테스트 함수명: `test_<조건>_<기대결과>` (예: `test_validate_grid_none_raises_invalid_size`).
- `@pytest.mark.parametrize` 로 형상 불일치(3×4, 4×3, 5×5) 묶음 실행.
- **RED 확인 전 구현 금지**; assertion 완화·`skip`·삭제로 GREEN 만들기 금지.
- fixture scope 기본 **`function`**; 행렬 fixture는 테스트 간 mutation 방지를 위해 매번 새 `list` 생성.

---

## 3. 경계값 케이스 목록

본 절의 케이스는 **입력이 Boundary에서 거부되어야 하는 경우**만 포함한다. **4×4 정상 입력은 의도적으로 제외**한다.

| TC ID | AC / Scenario | 입력 `grid` | 기대 결과 | PRD 코드 | Solver 호출 |
|---|---|---|---|---|---|
| **TC-BND-001** | **AC-FR-01-01** | `None` (명시적 None) | `BoundaryValidationError`, `INVALID_SIZE` / `ERR-BND-001` | ERR-BND-001 | **0회** |
| **TC-BND-002** | FR-01 형상 | `[]` (빈 리스트) | 동일 계열 형상 오류 | ERR-BND-002 | **0회** |
| **TC-BND-003** | FR-01 형상 | `[[]] * 4` (행 4개, 열 0) | 열 길이 0 → 4×4 아님 | ERR-BND-002 | **0회** |
| **TC-BND-004** | FR-01-AC-01 | `3×4` 행렬 (행 3, 열 4) | 형상 불일치 | ERR-BND-002 | **0회** |
| **TC-BND-005** | FR-01-AC-01 | `4×3` 행렬 (행 4, 열 3) | 형상 불일치 | ERR-BND-002 | **0회** |
| **TC-BND-006** | FR-01-AC-01 | `5×5` 행렬 | 형상 불일치 | ERR-BND-002 | **0회** |
| — | *(제외)* | `4×4` 정상 2빈칸 행렬 | — | — | 본 계획 **미포함** |

### 3.1 케이스별 상세 (Arrange 가이드)

#### TC-BND-001 — `grid=None` (앵커)

```python
grid = None
# Act: BoundaryValidator.validate(grid) 또는 validate_and_solve(grid) 경유
# Assert: pytest.raises(BoundaryValidationError) as exc
#   exc.value.error_code == "ERR-BND-001"  # 또는 INVALID_SIZE enum
#   "null" in exc.value.message.lower()
```

#### TC-BND-002 — `grid=[]`

- 행 개수 `len(grid) == 0` → 4×4 조건 위반 → `ERR-BND-002`.

#### TC-BND-003 — `grid=[[]] * 4`

- Python 참조 공유 주의: 4행 모두 `len(row)==0`.
- 검증 로직은 **각 행의 열 수**를 독립 검사해야 함 (동일 객체 참조에 의존하지 않음).

#### TC-BND-004 ~ 006 — 크기 불일치

| TC | Arrange 예시 |
|---|---|
| TC-BND-004 | `[[0]*4 for _ in range(3)]` |
| TC-BND-005 | `[[0]*3 for _ in range(4)]` |
| TC-BND-006 | `[[0]*5 for _ in range(5)]` |

### 3.2 파라미터화 예시 (pytest)

```python
import pytest

@pytest.mark.parametrize(
    "grid,expected_code",
    [
        (None, "ERR-BND-001"),
        ([], "ERR-BND-002"),
        ([[]] * 4, "ERR-BND-002"),
        ([[0] * 4 for _ in range(3)], "ERR-BND-002"),
        ([[0] * 3 for _ in range(4)], "ERR-BND-002"),
        ([[0] * 5 for _ in range(5)], "ERR-BND-002"),
    ],
    ids=[
        "none",
        "empty_list",
        "four_rows_zero_cols",
        "3x4",
        "4x3",
        "5x5",
    ],
)
def test_fr01_invalid_shape_rejects_grid(grid, expected_code):
    ...
```

---

## 4. 예외·특이 케이스 목록

Boundary 입력 검증 및 호출 경계에서 발생할 수 있는 **예외·비정상 입력**이다. (4×4 **정상** 입력 시나리오는 제외.)

| ID | 카테고리 | 입력·조건 | 기대 동작 | 비고 |
|---|---|---|---|---|
| **EX-01** | Null 참조 | `grid is None` | 즉시 `ERR-BND-001`, 이후 규칙 미평가 | AC-FR-01-01 앵커 |
| **EX-02** | 빈 컨테이너 | `grid == []` | `ERR-BND-002`, short-circuit | |
| **EX-03** | 래그드 행렬 | `[[1,2],[3,4,5]]` (가변 열 길이) | `ERR-BND-002` | 3×4/4×3 외 추가 권장 |
| **EX-04** | 제로 열 행 | `[[]]*4`, `[[],[],[],[]]` | `ERR-BND-002` | TC-BND-003 |
| **EX-05** | 비-리스트 타입 | `grid=42`, `grid="4x4"`, `grid={}` | `TypeError` 또는 `ERR-BND-002` | **Sprint 0 결정**: 공개 API가 `list[list[int]]`만 받으면 `TypeError`; pydantic DTO 사용 시 validation error로 통일 |
| **EX-06** | 중첩 깊이 오류 | `grid=[[[1]]]` | 형상/타입 오류 | P1 이후 |
| **EX-07** | 불변식 선행 | Boundary 실패 후 Control 호출 | `Solver.solve` **미호출** | mock 검증 필수 |
| **EX-08** | 오류 전파 | CLI/파사드가 Boundary 예외 포착 | 호출자에게 `error_code` 보존 | Integration (P3) |
| **EX-09** | 입력 불변 (NFR-04) | 검증 실패 경로 | 원본 `grid` 객체 변경 없음 | `None` 제외, mutable grid에 `copy` 검사 |
| **EX-10** | 이중 실패 금지 | `None` 입력 | Domain `BlankFinder` 등 **직접 호출 없음** | ECB: boundary→control만 |

### 4.1 pydantic 사용 시 (권장)

- Boundary 진입 DTO 예: `GridInput(rows: list[list[int]] | None)`.
- `grid=None` → ValidationError → Boundary에서 `ERR-BND-001`로 **매핑**하는 어댑터 테스트 추가.
- DTO 테스트는 Boundary 레이어에만 두고 **Entity는 pydantic 비의존** 유지.

---

## 5. Domain 해 결정 진입점 호출 횟수 검증 전략 (mock / spy)

### 5.1 “Domain 해 결정 진입점” 정의

| 구분 | 진입점 (검증 대상) | 레이어 |
|---|---|---|
| **Primary** | `Solver.solve(matrix)` 또는 `SolveUseCase.execute(matrix)` | Control |
| **Secondary** (spy 대상) | `BlankFinder.find`, `MissingNumberFinder.find`, `MagicSquareValidator.is_magic` | Entity |

**정책 (PRD §13):** Boundary 입력 검증 실패 시 **Primary 진입점 호출 0회**. Secondary는 Primary를 통해서만 호출되므로 Primary mock으로 간접 보장.

### 5.2 전략 A — `unittest.mock.patch` (권장, P0)

**대상:** Control의 `Solver.solve` (또는 유스케이스 파사드).

```python
from unittest.mock import patch
import pytest

@pytest.mark.parametrize("grid", [None, [], [[]] * 4], ids=["none", "empty", "zero_cols"])
def test_boundary_failure_does_not_invoke_solver(grid):
    with patch("MagicSquare.control.use_cases.solver.Solver.solve") as mock_solve:
        with pytest.raises(BoundaryValidationError):
            boundary_entry(grid)  # CLI 또는 BoundaryValidator 래퍼

        mock_solve.assert_not_called()
```

- **패치 경로**: 테스트 대상이 import하는 **사용처 네임스페이스**에 patch (`where it's used`).
- Integration 테스트: `patch` 대상을 파사드 내부의 `Solver` 인스턴스 메서드로 좁힌다.

### 5.3 전략 B — Spy (호출 횟수 명시)

```python
mock_solve.assert_called_once()  # 성공 경로 전용 — 본 계획서 성공 케이스 제외
mock_solve.call_count == 0       # TC-BND-001~006 공통
```

### 5.4 전략 C — Fake Boundary + Real Control (역방향 금지)

- Boundary를 Fake로 두고 Control만 실제 — **금지** (ECB 위반: 실패 정책은 Boundary 책임).
- 올바른 방향: **Real Boundary + Mock Control Solver**.

### 5.5 Entity 직접 호출 누출 검测 (선택, P1)

```python
with (
    patch("...Solver.solve") as mock_solve,
    patch("...BlankFinder.find") as mock_blank,
):
    ...
    mock_solve.assert_not_called()
    mock_blank.assert_not_called()
```

### 5.6 검증 매트릭스

| TC ID | `Solver.solve` | `BlankFinder.find` |
|---|---|---|
| TC-BND-001 ~ 006 | 0 | 0 (선택 assert) |

---

## 6. 커버리지 목표

| 대상 | 목표 | 근거 | 측정 범위 |
|---|---|---|---|
| **Domain** (`entity` + `control` solver 로직) | **≥ 95%** | NFR-01, Epic | `MagicSquare.entity`, `MagicSquare.control` |
| **Boundary** (`boundary` 검증·출력) | **≥ 85%** | NFR-02 | `MagicSquare.boundary` |
| **프로젝트 전체** | **≥ 80%** | NFR-08, Cursor Rules | 패키지 전체 |

### 6.1 본 계획서(P0)와 커버리지의 관계

- P0만 구현 시 Domain 95%는 **미달 가능** — Track B RED와 병행 필요.
- P0 완료 시 Boundary의 `validate` 분기(null, row/col count)는 **85% 달성을 우선** 목표로 한다.

### 6.2 미커버 허용하지 않는 분기 (Boundary)

- `grid is None` 분기
- `len(rows) != GRID_SIZE` 분기
- `any(len(row) != GRID_SIZE for row in grid)` 분기
- 검증 실패 시 early return / raise 경로

---

## 7. pytest-cov 측정 전략

### 7.1 설치

```bash
pip install pytest-cov
```

개발 의존성으로 고정 시 `pyproject.toml` 예:

```toml
[project.optional-dependencies]
dev = ["pytest>=8.0", "pytest-cov>=5.0", "pydantic>=2.0"]
```

### 7.2 실행 명령 (사용자 지정 형식)

```bash
pytest --cov=src --cov-report=term-missing
```

### 7.3 패키지 경로 정합 (ECB 레이아웃)

현재 저장소 규칙은 루트 패키지 `MagicSquare/` 이다. `src` 레이아웃을 채택할 경우:

```
src/
└── MagicSquare/
    ├── boundary/
    ├── control/
    └── entity/
```

**권장 cov 타깃 (레이어별 게이트):**

```bash
# Boundary ≥ 85%
pytest tests/boundary --cov=MagicSquare.boundary --cov-report=term-missing --cov-fail-under=85

# Domain (entity + control) ≥ 95%
pytest tests/entity tests/control \
  --cov=MagicSquare.entity --cov=MagicSquare.control \
  --cov-report=term-missing --cov-fail-under=95

# 전체 ≥ 80%
pytest --cov=MagicSquare --cov-report=term-missing --cov-fail-under=80
```

`--cov=src` 사용 시: `src` 아래에 `MagicSquare`가 있어야 하며, CI에서는 **동일 기준을 레이어별 job으로 분리**하는 것을 권장한다.

### 7.4 term-missing 해석 (P0 예시)

```
MagicSquare/boundary/validators/boundary_validator.py    85%   12-15, 22-24
```

- **12-15**: `None` 검사 분기 — TC-BND-001 미실행 시 표시
- **22-24**: 열 길이 검사 — TC-BND-003, 004~006 미실행 시 표시

### 7.5 CI·로컬 게이트 (권장)

| 단계 | 명령 | 실패 조건 |
|---|---|---|
| PR 빠른 검증 | `pytest tests/boundary -q` | 테스트 실패 |
| Boundary 게이트 | `--cov=MagicSquare.boundary --cov-fail-under=85` | 커버리지 < 85% |
| Domain 게이트 | `--cov=MagicSquare.entity --cov=MagicSquare.control --cov-fail-under=95` | 커버리지 < 95% |
| 전체 | `--cov=MagicSquare --cov-fail-under=80` | 커버리지 < 80% |

### 7.6 측정에서 제외할 항목 (선택)

- `tests/**`, `**/__init__.py` (빈 파일만인 경우)
- `if TYPE_CHECKING:` 블록
- CLI `main` 가드 (`if __name__ == "__main__"`)

---

## 8. 추적성 (Traceability)

| Test Case | AC / Scenario | FR | Business Rule | Component |
|---|---|---|---|---|
| TC-BND-001 | **AC-FR-01-01** / SC-BND-001 | FR-01 | BR-01 | BoundaryValidator |
| TC-BND-002~003 | SC-BND-002 | FR-01 | FR-01-AC-01, BR-01 | BoundaryValidator |
| TC-BND-004~006 | SC-BND-002 | FR-01 | FR-01-AC-01, BR-01 | BoundaryValidator |
| Solver 0-call | FR-01-AC-05 | FR-01 | — | Solver (mock) |

---

## 9. RED → GREEN → REFACTOR 체크리스트 (P0)

| 단계 | 작업 | 완료 조건 |
|---|---|---|
| **RED** | `test_validate_grid_none_raises_err_bnd_001` 작성 | `pytest` 실패, 이유가 “미구현” |
| **RED** | TC-BND-002~006 + parametrize 추가 | 의도된 실패 다수 |
| **RED** | `test_boundary_failure_solver_not_called` | mock이 “호출됨”으로 실패 |
| **GREEN** | `BoundaryValidator` 최소 구현 (null → 4×4 순) | P0 테스트 GREEN |
| **GREEN** | 파사드에서 Solver 호출 전 검증 | mock 0-call GREEN |
| **REFACTOR** | 상수 추출 (`GRID_SIZE=4`), 메시지 템플릿 통일 | 전체 pytest GREEN, Boundary cov ≥ 85% |

---

## 10. 참고 문서

| 문서 | 용도 |
|---|---|
| `docs/PRD_MagicSquare.md` | FR-01, ERR-BND-*, NFR-01/02/08 |
| `Report/07.magic_square_tdd_readme_todo_report.md` | SC-BND-001, Dual-Track 순서 |
| `.cursor/rules/magicsquare-*.mdc` | ECB, TDD, 금지 패턴 |

---

*본 문서는 구현 전 테스트 설계 산출물이며, 4×4 정상·Solver 성공 경로는 별도 Test Plan (Track B / Integration)에서 다룬다.*
