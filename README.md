# Magic Square XX — 4×4 마방진 퍼즐 검증 시스템

> 사용자가 4×4 격자에 숫자를 직접 입력하면,
> 프로그램이 마방진 조건을 검증하고 구체적인 피드백을 제공하는 시스템.

---

## 프로젝트 개요

| 항목 | 내용 |
|---|---|
| **프로젝트명** | Magic_Square_XX |
| **유형** | 퍼즐 검증 시스템 (User-Fill Puzzle Validator) |
| **격자 크기** | 4×4 (16칸) |
| **사용 숫자 범위** | 1 이상 16 이하 (중복 없음) |
| **기준값 S** | 34 (행·열·대각선의 공통 합) |
| **설계 방식** | TDD (Test-Driven Development) |

---

## 문제 정의

### 핵심 Invariant

모든 유효한 4×4 마방진 M에 대해 다음 조건이 참이어야 한다.

```
① M의 모든 원소는 서로 다르며 1 이상 16 이하의 값이다.
② 임의의 행 i에 대해:   sum(M[i][*]) = 34
③ 임의의 열 j에 대해:   sum(M[*][j]) = 34
④ 주대각선의 합         = 34
⑤ 반대각선의 합         = 34
⑥ 기준값 S = 34는 숫자 집합에 의해 결정되며, 임의로 지정되지 않는다.
```

> 조건 ①이 선행되지 않으면 ②~⑥은 의미가 없다.
> **조건의 순서와 의존 관계가 설계의 구조를 결정한다.**

### 개선된 문제 정의

> "사용자가 4×4 격자에 숫자를 직접 입력했을 때,
> 프로그램은 그 배치가 행·열·두 대각선의 합이 모두 동일하다는 조건을 만족하는지를 검증하고,
> 조건 위반 시 **어디서, 무엇이, 얼마나** 틀렸는지를 명확히 식별하여 사용자에게 알려준다."

---

## 시스템 입력/출력 경계

```
입력:  사용자가 직접 채운 4×4 배치 (16개의 숫자)
           │
           ▼
     [ 검증 시스템 ]
           │
           ▼
출력:  ① 전체 합격(PASS) / 불합격(FAIL) 판정
       ② 불합격 시 — 어떤 행/열/대각선이 조건을 위반했는가
       ③ 불합격 시 — 중복 또는 범위 위반이 있는가
```

---

## 검증 명세 (Validation Specification)

| ID | 검사명 | 조건 | 위반 시 동작 | 이후 진행 |
|---|---|---|---|---|
| VS-01 | 완전성 | 16개 칸 모두 채워짐 | 중단 + 빈 칸 위치 피드백 | 중단 |
| VS-02 | 유일성 | 중복 값 없음 | 중단 + 중복값·위치 피드백 | 중단 |
| VS-03 | 범위 | 1 이상 16 이하 | 중단 + 초과값·위치 피드백 | 중단 |
| VS-04 | 행 합 | 각 행의 합 = 34 | 위반 기록 후 계속 | 계속 |
| VS-05 | 열 합 | 각 열의 합 = 34 | 위반 기록 후 계속 | 계속 |
| VS-06 | 대각선 합 | 양 대각선의 합 = 34 | 위반 기록 후 계속 | 계속 |

### 검증 흐름

```
사용자 입력
    │
    ▼
VS-01 완전성 ── FAIL ──► 검증 중단 + 피드백
    │ PASS
    ▼
VS-02 유일성 ── FAIL ──► 검증 중단 + 피드백
    │ PASS
    ▼
VS-03 범위   ── FAIL ──► 검증 중단 + 피드백
    │ PASS
    ▼
VS-04 행 합  ── 위반 기록 (계속 진행)
    │
    ▼
VS-05 열 합  ── 위반 기록 (계속 진행)
    │
    ▼
VS-06 대각선 ── 위반 기록
    │
    ▼
위반 없음 ──► PASS
위반 있음 ──► FAIL + 전체 위반 목록 피드백
```

> **VS-01 ~ VS-03** : 선행 조건 — 실패 시 즉시 중단
> **VS-04 ~ VS-06** : 독립 조건 — 실패해도 모두 검사 후 통합 피드백 제공

---

## 기능 요구사항 (Functional Requirements)

| ID | 요구사항 |
|---|---|
| FR-01 | 사용자로부터 4×4 크기의 숫자 배치를 입력받아야 한다 |
| FR-02 | 입력된 배치에 대해 VS-01부터 VS-06 순서대로 검증을 수행해야 한다 |
| FR-03 | 검증 결과로 PASS 또는 FAIL을 반환해야 한다 |
| FR-04 | FAIL인 경우, 어디서·무엇이·얼마나 틀렸는지를 구체적으로 알려야 한다 |

## 비기능 요구사항 (Non-Functional Requirements)

| 항목 | 요구사항 |
|---|---|
| 피드백 명확성 | 위반 메시지는 행/열 번호와 실제 합·기대값을 포함해야 한다 |
| 검증 순서 일관성 | 동일한 입력에 대해 항상 동일한 순서로 검증이 진행되어야 한다 |
| 독립성 | 각 검증 단계는 다른 단계의 내부 구현에 의존하지 않아야 한다 |
| 확장성 | 숫자 범위나 격자 크기 변경 시 검증 구조가 크게 바뀌지 않아야 한다 |

---

## 경계 조건 (Edge Cases)

| 입력 상황 | 분류 | 탐지 단계 |
|---|---|---|
| 0 입력 | 범위 위반 | VS-03 |
| 음수 입력 | 범위 위반 | VS-03 |
| 17 이상의 값 입력 | 범위 위반 | VS-03 |
| 같은 값이 두 칸 이상 존재 | 유일성 위반 | VS-02 |
| 행 합은 맞지만 열 합이 틀림 | 열 조건 위반 | VS-05 |
| 모든 합이 맞지만 대각선만 틀림 | 대각선 조건 위반 | VS-06 |
| 완벽한 마방진 입력 | PASS | 전 단계 통과 |

---

## 용어 정의 (Glossary)

| 용어 | 정의 |
|---|---|
| **배치(Arrangement)** | 사용자가 4×4 격자에 입력한 16개 숫자의 집합 |
| **기준값 S** | 마방진이 성립할 때 모든 행·열·대각선이 가져야 하는 공통 합 (= 34) |
| **검증(Validation)** | 배치가 마방진 조건을 만족하는지 판정하는 행위 |
| **판정(Verdict)** | 검증의 최종 결과 — PASS 또는 FAIL |
| **위반(Violation)** | 특정 조건을 만족하지 못하는 상태 |
| **피드백(Feedback)** | 위반 발생 시 사용자에게 전달되는 구체적 정보 |
| **Invariant** | 시스템이 어떤 상태에서도 반드시 지켜야 하는 불변 조건 |

---

## 프로젝트 구조

```
Magic_Square_XX/
├── README.md                          ← 이 파일
├── Report/
│   └── problem_definition_report.md  ← 문제 정의 보고서
└── Prompting/
    └── 01.problem_definition_report-Prompt.md  ← 대화형 프롬프트 트랜스크립트
```

---

## 개발 로드맵

| 단계 | 내용 | 상태 |
|---|---|---|
| 1. 문제 인식 | 관찰 → Why 분석 → 진짜 문제 정의 | 완료 |
| 2. 요구사항 명세 | FR, VS, Edge Cases, 비기능 요구사항 | 완료 |
| 3. TDD 설계 | 검증 명세 기반 테스트 케이스 설계 (코드 작성 전) | 예정 |
| 4. 인터페이스 설계 | 사용자 입력 방식 결정 | 예정 |
| 5. 구현 | TDD 설계 기반 실제 코드 작성 | 예정 |
| 6. 검증 | 전체 테스트 통과 확인 | 예정 |

---

## RED 단계 To-Do 리스트

> 이 체크리스트는 test_plan.md 기반으로 생성되었습니다.
> 각 항목은 RED(실패 테스트 작성) 완료 시 체크합니다.

### Track A — UI / Boundary 테스트
- [ ] TC-A-01: grid=None 입력 → 실패 결과 반환 (Happy Path of Failure)
- [ ] TC-A-02: code가 정확히 "INVALID_SIZE" 문자열인지 검증
- [ ] TC-A-03: message가 "Grid must be 4x4." 와 문자 단위 동일한지 검증
- [ ] TC-A-04: grid=None 시 Domain 진입점 0회 호출 (mock/spy 검증)
- [ ] TC-A-05: grid=[] 빈 리스트 → 실패 결과 반환
- [ ] TC-A-06: grid=3×4 크기 불일치 → 실패 결과 반환
- [ ] TC-A-07: 반환 객체 타입이 지정 실패 결과 구조체인지 검증

### Track B — Domain / Logic 테스트
- [ ] TC-B-01: resolve()가 None grid를 직접 받지 않음을 격리 검증
- [ ] TC-B-02: Boundary가 None 분기를 처리 후 resolve() 미호출 확인
- [ ] TC-B-03: resolve() mock이 호출됐을 경우 테스트 실패 처리
- [ ] TC-B-04: AC-FR-01-02~05 범위의 케이스는 이 커밋에 포함하지 않음 확인

### 커버리지 목표
- [ ] Domain Logic: 95%+ (pip install pytest-cov)
- [ ] Boundary Layer: 85%+
- [ ] 전체 TOTAL: 90%+

### 결함 목록 연결
- [x] defect_list.md 생성 및 발견 결함 기록
- [ ] 모든 결함 수정 후 회귀 테스트 통과 확인

---

## REFACTOR 단계 To-Do 리스트

> 기준: `.cursor/rules/magicsquare-tdd-testing.mdc` — **모든 테스트 통과 후** 내부 구조만 개선, 기능 변경 금지.
> 테스트 없이 리팩터링을 시작하면 회귀를 검증할 안전망이 없으므로, 각 항목은 선행 GREEN 테스트 완료 후 진행한다.

### 선행 조건 (REFACTOR 전 GREEN)

- [ ] RF-P0: DEF-003 수정 — `test_isolation_module_does_not_patch_blank_finder` → control 21/21 GREEN
- [ ] RF-P1: `boundary_validator` valid 4×4 success path — 신규 GREEN 테스트 작성 후 `NotImplementedError` 제거 (DEF-004)
- [ ] RF-P2: `tests/entity/test_d_sol.py` D-SOL-01~04 GREEN — `Solver.resolve()` 로직 구현/리팩터 선행
- [ ] RF-P3: `tests/control/test_solver.py` 신규 작성 — `Solver.resolve(valid_4x4)` 계약 단위 테스트

### `src/boundary/validators/boundary_validator.py`

- [ ] RF-BV-01: `_has_invalid_shape` private 메서드 추출·정리 (null/형상 실패 동작 불변)
- [ ] RF-BV-02: 실패 DTO 생성 로직 정리 (`ValidationFailureResult` 팩토리 또는 헬퍼 추출)
- [ ] RF-BV-03: valid 4×4 → success sentinel 반환 (RF-P1 GREEN 후, facade 연동)

### `src/control/use_cases/solver.py`

- [ ] RF-SL-01: `tests/entity/test_d_sol.py` → `tests/control/` 이동, `solution` → `Solver.resolve` import 정렬
- [ ] RF-SL-02: `Solver.resolve()` 내부 구조 리팩터 (RF-P2 GREEN 후, D-SOL-01~04 통과 유지)
- [ ] RF-SL-03: facade 통합 테스트 — valid 4×4 → boundary success → `resolve` 1회 호출

### 연관 — `src/boundary/facade.py`

- [ ] RF-FC-01: `validate_and_solve` 반환 타입 union 도입 (`ValidationFailureResult | SolveSuccessResult`, RF-BV-03 후)
- [ ] RF-FC-02: orchestration 정리 — boundary success 분기에서만 `Solver.resolve` 호출 (RF-BV-03 후)

### 구조·품질 (기능 불변)

- [ ] RF-001: `INVALID_SIZE_*` 상수 중복 제거 — `tests/conftest.py`가 `boundary.constants` import
- [ ] RF-002: 패키지 레이아웃 통일 — `entity/`(root) vs `src/boundary|control` → pytest.ini·test_plan·import 일괄 정렬
- [ ] RF-003: `entity/models/user.py` ECB 예제 — entity services GREEN 후 `examples/` 분리 검토
- [ ] RF-004: 도메인 상수 중앙화 — S=34, 1..16 → `entity/constants.py` (`MAGIC_SUM`, `MIN_CELL`, `MAX_CELL`)

### REFACTOR 완료 검증

- [ ] RF-V01: `pytest tests/boundary/test_boundary_validator_ac_fr_01_01.py` 회귀 통과
- [ ] RF-V02: `pytest tests/control/` 전체 GREEN (DEF-003 포함)
- [ ] RF-V03: 커버리지 80% 이상 유지 또는 향상

---

*최초 작성: 2026-05-28*
