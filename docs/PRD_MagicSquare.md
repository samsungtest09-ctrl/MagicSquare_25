# PRD — Magic Square 4x4 TDD Practice

## 1. Executive Summary

Magic Square 4x4 TDD Practice는 알고리즘 난이도보다 **불변식 기반 설계·검증 사고**, **입력/출력 계약 고정**, **Dual-Track UI + Logic TDD**, **설계 → RED → GREEN → REFACTOR → 회귀 보호** 흐름을 훈련하는 학습용 프로젝트이다. 시스템은 정확히 빈칸 2개(`0`)를 포함한 4×4 정수 행렬을 입력받아, 누락된 두 숫자를 두 가지 배치 순서(small-first, reverse)로 시도한 뒤 마방진이 성립하는 조합을 찾아 `[r1, c1, n1, r2, c2, n2]` 형식의 6원소 정수 배열(1-index 좌표)을 반환한다. UI·DB·Web 없이 콘솔/테스트 실행 중심으로 Boundary(입력 검증·출력 계약)와 Domain(불변식·풀이 로직)을 분리하고, Concept → Rule → Use Case → Contract → Test → Component 추적성을 유지한다.

**훈련 핵심 역량**

- 불변식 사고: 행·열·대각선 합, 값 범위, 중복, 빈칸 규칙을 선행 조건으로 고정
- 입력/출력 계약: 모호한 요구 대신 검증 가능한 계약으로 RED 테스트 작성
- Dual-Track TDD: Boundary Track과 Domain Track을 병렬·독립 RED-GREEN-REFACTOR
- 설계 → 테스트 → 구현 → 리팩토링: 계약 불변 상태에서 내부 구조만 개선

---

## 2. Background

Report/01(문제 정의)에 따르면, 4×4 마방진 문제는 “숫자를 채운다”는 표면 목표보다 **행·열·대각선 합이 동일하다는 불변 조건을 자동 검증하는 시스템**을 설계하는 것이 본질이다. 학습자는 조건을 암묵적으로 적용하고, 수동으로 합을 계산하며, 검증 기준이 불명확한 상태에서 구현을 먼저 시작하는 문제를 겪는다.

본 PRD는 Report/01의 **퍼즐 검증·피드백** 맥락에서 출발하되, Report/02·Report/05 및 고정 입출력 계약에 따라 범위를 **2빈칸 Solver + 계약 기반 TDD 훈련**으로 한정한다. 즉, “완전한 16칸 PASS/FAIL 검증기”가 아니라, **검증 가능한 불변식 조건을 만족하는 해를 찾아 고정 출력 형식으로 반환하는 순수 로직 시스템**을 목표로 한다.

---

## 3. Problem Statement

본 프로젝트의 문제는 “4×4 마방진을 만든다”가 아니라 **“주어진 부분 행렬이 마방진 불변식을 만족하도록 누락 숫자를 배치할 수 있는지 검증 가능하게 판정하고, 성공 시 계약된 좌표·숫자 순서로 결과를 반환한다”**는 것이다.

입력/출력 계약이 핵심인 이유:

- TDD에서 RED 테스트는 **특정 입력 → 특정 출력/실패**를 선언해야만 작성 가능하다.
- 계약이 없으면 Boundary와 Domain 책임, 실패 정책, 테스트 데이터가 분리되지 않는다.
- 리팩토링 후에도 외부 계약(배열 길이 6, 1-index, 시도 순서)이 회귀 테스트로 보호되어야 한다.

---

## 4. Why Now / Why Chain

| Why | 설명 |
|---|---|
| Why #1 — 마방진 완성 | 사용자(학습자)는 부분 채워진 격자에서 누락 숫자 배치가 올바른지 즉시 판단할 수 없다. |
| Why #2 — 프로그램 구현 | 불변식 검증과 조합 시도를 오차 없이 반복 실행해야 한다. |
| Why #3 — TDD 방식 | “무엇이 참인가”를 테스트로 먼저 고정해야 Boundary/Domain 분리와 회귀 보호가 가능하다. |

**학습자 Pain Point → PRD 대응**

| Pain Point | PRD 대응 |
|---|---|
| 구현 먼저 시작 | FR·BR·Contract·Test Plan을 구현 전 기준으로 고정 |
| 테스트 기준 불명확 | 모든 FR에 Acceptance Criteria와 Traceability Matrix 연결 |
| Boundary/Domain 혼합 | ECB 의존 방향 및 FR별 Layer 명시 |
| 리팩토링 후 계약 붕괴 | Dual-Track TDD + REFACTOR 단계 회귀 테스트 의무 |

---

## 5. Target Users

| Persona | 목적 | 사용 환경 |
|---|---|---|
| TDD 학습자 | RED-GREEN-REFACTOR 루프 훈련 | `pytest` 실행, CLI 호출 |
| 코드 리뷰어 | 계약·레이어·테스트 추적성 검증 | PR, Traceability Matrix |
| Clean Architecture/ECB 학습자 | Boundary-Control-Entity 분리 실습 | 로컬 개발, 테스트 중심 |

**범위 밖 사용자 환경:** UI 화면, DB, Web/API 서버, 외부 인증

---

## 6. Vision & Epic Goal

**Epic:** 불변식 기반 사고 훈련 시스템 구축 (Report/05 Level 1)

**Epic Goal**

- 4×4 Magic Square 2빈칸 Solver를 통해 불변식 중심 설계를 훈련한다.
- Dual-Track UI + Logic TDD 흐름을 경험한다.
- 입력/출력 계약을 먼저 정의하고 리팩토링 후에도 외부 계약을 유지한다.

**Epic Success Criteria (검증 가능)**

- Domain Logic 테스트 커버리지 ≥ 95%
- Boundary 입력 검증 계약 테스트 100% 통과
- Domain/Business Rule과 테스트 간 Traceability Matrix 완전 연결
- 매직 넘버 하드코딩 없이 명명 상수(`GRID_SIZE`, `BLANK_VALUE`, `MIN_VALUE`, `MAX_VALUE`, `MAGIC_CONSTANT`, `EXPECTED_BLANK_COUNT`, `OUTPUT_LENGTH`) 사용

---

## 7. Persona

**Primary Persona: TDD 학습 중인 개발자**

- 알고리즘 정답 암기보다 설계·계약·테스트·리팩토링 흐름을 훈련하려 한다.
- Clean Architecture ECB 계층 분리를 코드 구조로 확인하려 한다.
- 실패 케이스(입력 오류, unsolvable)를 테스트로 먼저 고정하려 한다.

---

## 8. User Journey Summary

| Stage | Action | Pain Point | Learning Outcome |
|---|---|---|---|
| 1. Problem Recognition | 2빈칸 Solver 계약과 불변식 목록 확인 | “마방진 만든다”는 모호한 목표 | 불변식·계약 중심 문제 정의 |
| 2. Contract Definition | Input/Output Contract, Error Code 확정 | 0-index/1-index, row-major 혼동 | 테스트 가능한 계약 문서화 |
| 3. Domain Separation | Boundary vs Entity vs Control 책임 분리 | 검증과 풀이 로직 혼합 | ECB 의존 방향 준수 |
| 4. Dual-Track TDD | Track A/B 각각 RED→GREEN→REFACTOR | Domain 전부 구현 후 Boundary 붙이기 | 병렬 최소 구현 + 회귀 보호 |
| 5. Regression Protection | REFACTOR 후 전체 pytest 재실행 | 리팩토링 후 silent contract break | 계약 불변 + 커버리지 유지 |

---

## 9. Scope

### 9.1 In-Scope

- 4×4 정수 행렬 입력 수용 및 Boundary 입력 검증
- row-major 기준 첫 번째·두 번째 빈칸(`0`) 좌표 탐색
- 누락 숫자 2개 탐색 및 오름차순 정렬
- 완성 행렬에 대한 마방진 판정(행·열·대각선 합 = 34)
- small-first → reverse 두 조합 시도 및 결과 포맷팅
- 입력 검증 실패 시 Domain resolver 미호출
- RED-GREEN-REFACTOR에 맞는 테스트 가능 요구사항·시나리오·추적성

### 9.2 Out-of-Scope

- UI 화면 개발
- DB 저장/검색
- Web/API 서버 개발
- N×N 일반화
- 완전한 마방진 생성 알고리즘(임의 크기 생성)
- 사용자 인증/권한
- 네트워크 오류 처리
- QR 스캔
- 외부 서비스 연동
- Report/01의 16칸 완전 채움 PASS/FAIL 피드백 검증기(별도 Epic)

---

## 10. Functional Requirements

### FR-01 Input Verification (Boundary)

- **Description:** Boundary는 Solver 호출 전 입력 행렬이 고정 입력 계약을 만족하는지 검증한다.
- **Layer:** Boundary
- **Input:** `int[][]` (nullable 아님을 전제; `None` 입력은 별도 오류 — SC-BND-001)
- **Processing Rules:**
  1. 행렬이 `None`이면 `ERR-BND-001`로 즉시 실패한다.
  2. 행렬이 정확히 4행 4열이 아니면 `ERR-BND-002`로 즉시 실패한다.
  3. `0`의 개수가 정확히 2가 아니면 `ERR-BND-003`으로 즉시 실패한다.
  4. 모든 값이 `0` 또는 `1~16` 범위가 아니면 `ERR-BND-004`로 즉시 실패한다.
  5. `0`을 제외한 값에 중복이 있으면 `ERR-BND-005`로 즉시 실패한다.
  6. 위 검증 실패 시 Control/Domain Solver는 호출되지 않는다.
- **Output:** 검증 성공 시 Control에 유효 행렬 전달; 실패 시 `BoundaryValidationError`(error_code 포함) 발생
- **Acceptance Criteria:**
  - **FR-01-AC-01:** 4×4가 아닌 행렬 입력 시 `ERR-BND-002`가 발생하고 Solver가 호출되지 않는다.
  - **FR-01-AC-02:** 빈칸(`0`) 개수가 2가 아니면 `ERR-BND-003`이 발생하고 Solver가 호출되지 않는다.
  - **FR-01-AC-03:** `0` 또는 `1~16` 범위를 벗어난 값이 있으면 `ERR-BND-004`가 발생하고 Solver가 호출되지 않는다.
  - **FR-01-AC-04:** `0`을 제외한 중복 값이 있으면 `ERR-BND-005`가 발생하고 Solver가 호출되지 않는다.
  - **FR-01-AC-05:** 모든 검증 규칙을 통과한 입력만 Control Solver Use Case로 전달된다.
- **Error / Exception Policy:** Boundary 검증 실패는 `BoundaryValidationError(error_code, message)`로 표준화한다.
- **Related Business Rules:** BR-01, BR-02, BR-03, BR-04
- **Related Test Direction:** SC-BND-002~005, Track A RED
- **Component Candidate:** BoundaryValidator

---

### FR-02 Blank Coordinate Discovery

- **Description:** Domain은 row-major 순서로 첫 번째·두 번째 빈칸 좌표를 1-index로 반환한다.
- **Layer:** Entity (Domain)
- **Input:** FR-01을 통과한 `int[4][4]`
- **Processing Rules:**
  1. 행 1→4, 각 행에서 열 1→4 순으로 스캔한다.
  2. 값이 `0`인 첫 좌표를 첫 번째 빈칸 `(r1, c1)`으로 기록한다.
  3. 값이 `0`인 두 번째 좌표를 두 번째 빈칸 `(r2, c2)`으로 기록한다.
  4. 반환 좌표는 1-index이다.
- **Output:** `(r1, c1, r2, c2)` — 각 값은 `1~4` 정수
- **Acceptance Criteria:**
  - **FR-02-AC-01:** row-major 첫 `0`의 1-index 좌표가 `(r1, c1)`으로 반환된다.
  - **FR-02-AC-02:** row-major 두 번째 `0`의 1-index 좌표가 `(r2, c2)`으로 반환된다.
  - **FR-02-AC-03:** 빈칸이 정확히 2개일 때만 좌표 2쌍이 반환된다(선행 조건은 FR-01).
- **Error / Exception Policy:** FR-01 통과 입력만 처리; 빈칸 개수 오류는 FR-01에서 차단
- **Related Business Rules:** BR-02, BR-05
- **Related Test Direction:** SC-DOM-001, Track B RED
- **Component Candidate:** BlankFinder

---

### FR-03 Missing Number Discovery

- **Description:** Domain은 `1~16` 중 행렬에 존재하지 않는 정확히 2개의 누락 숫자를 오름차순으로 반환한다.
- **Layer:** Entity (Domain)
- **Input:** FR-01을 통과한 `int[4][4]`
- **Processing Rules:**
  1. `1~16` 집합에서 행렬에 등장한 값(`0` 제외)을 제외한다.
  2. 남은 값이 정확히 2개여야 한다.
  3. 두 값을 오름차순 `[small, large]`로 반환한다.
- **Output:** `(small, large)` where `small < large`
- **Acceptance Criteria:**
  - **FR-03-AC-01:** 누락 숫자는 정확히 2개이다.
  - **FR-03-AC-02:** 반환 순서는 오름차순(`small`, `large`)이다.
  - **FR-03-AC-03:** `small`과 `large`는 `1~16` 범위이며 행렬에 존재하지 않는다.
- **Error / Exception Policy:** 누락 숫자 개수 ≠ 2는 FR-01/중복·범위 검증과 모순되므로 Domain 단독 호출 전 Boundary에서 차단됨
- **Related Business Rules:** BR-06, BR-07
- **Related Test Direction:** SC-DOM-002, Track B RED
- **Component Candidate:** MissingNumberFinder

---

### FR-04 Magic Square Validation

- **Description:** Domain은 16칸이 모두 채워진 4×4 행렬이 마방진 불변식을 만족하는지 판정한다.
- **Layer:** Entity (Domain)
- **Input:** `int[4][4]` (모든 값 `1~16`, 중복 없음, `0` 없음)
- **Processing Rules:**
  1. 4개 행 각각의 합이 `MAGIC_CONSTANT(34)`와 같아야 한다.
  2. 4개 열 각각의 합이 `34`와 같아야 한다.
  3. 주대각선 합이 `34`와 같아야 한다.
  4. 반대각선 합이 `34`와 같아야 한다.
  5. 위 4조건이 모두 참이면 `true`, 하나라도 거짓이면 `false`를 반환한다.
- **Output:** `boolean`
- **Acceptance Criteria:**
  - **FR-04-AC-01:** 알려진 유효 4×4 마방진 전체 행렬 입력 시 `true`를 반환한다.
  - **FR-04-AC-02:** 행 합이 34가 아닌 행렬 입력 시 `false`를 반환한다.
  - **FR-04-AC-03:** 열 합이 34가 아닌 행렬 입력 시 `false`를 반환한다.
  - **FR-04-AC-04:** 대각선 합이 34가 아닌 행렬 입력 시 `false`를 반환한다.
- **Error / Exception Policy:** 판정 실패는 예외가 아닌 `false` 반환
- **Related Business Rules:** BR-08, BR-09
- **Related Test Direction:** SC-DOM-003~005, Track B RED
- **Component Candidate:** MagicSquareValidator

---

### FR-05 Two-Combination Solver and Result Formatting

- **Description:** Control은 두 배치 조합을 순서대로 시도하고, 성공 시 Boundary 출력 계약에 맞는 `int[6]`을 반환한다. Boundary는 최종 출력 형식을 검증한다.
- **Layer:**
  - **Control:** Solver 오케스트레이션 (Attempt 1 → Attempt 2)
  - **Entity:** 조합 생성·마방진 판정
  - **Boundary:** 성공 결과 `[r1,c1,n1,r2,c2,n2]` 형식 보장
- **Input:** FR-01 통과 행렬
- **Processing Rules:**
  1. BlankFinder로 `(r1,c1,r2,c2)` 획득
  2. MissingNumberFinder로 `(small, large)` 획득
  3. **Attempt 1 (small-first):** `(r1,c1)←small`, `(r2,c2)←large` 임시 완성 행렬 생성 → MagicSquareValidator 검사 → 성공 시 `[r1,c1,small,r2,c2,large]` 반환
  4. **Attempt 2 (reverse):** Attempt 1 실패 시 `(r1,c1)←large`, `(r2,c2)←small` → 검사 → 성공 시 `[r1,c1,large,r2,c2,small]` 반환
  5. 두 Attempt 모두 실패 시 `ERR-DOM-001` (`UnsolvableCombinationError`)
  6. 입력 행렬 원본은 변경하지 않는다(내부 작업은 복사본 사용).
- **Output:** `int[6]` = `[r1, c1, n1, r2, c2, n2]` (1-index, 길이 6)
- **Acceptance Criteria:**
  - **FR-05-AC-01:** Attempt 1이 마방진이면 `[r1,c1,small,r2,c2,large]`를 반환한다.
  - **FR-05-AC-02:** Attempt 1 실패·Attempt 2 성공 시 `[r1,c1,large,r2,c2,small]`를 반환한다.
  - **FR-05-AC-03:** 두 Attempt 모두 실패 시 `ERR-DOM-001`이 발생한다.
  - **FR-05-AC-04:** 반환 배열 길이는 항상 6이다.
  - **FR-05-AC-05:** `r1,c1,r2,c2`는 1-index이며 `1~4` 범위이다.
  - **FR-05-AC-06:** Solver 실행 전후 입력 행렬 값·형상이 변경되지 않는다.
- **Error / Exception Policy:** Domain unsolvable → `UnsolvableCombinationError(ERR-DOM-001)`; Boundary가 호출자에게 전파
- **Related Business Rules:** BR-05~BR-12
- **Related Test Direction:** SC-CTL-001~003, SC-BND-006~007, TD-001, TD-002
- **Component Candidate:** Solver (Control), ResultFormatter (Boundary)

---

## 11. Business Rules / Domain Rules

| ID | Rule (항상 참) |
|---|---|
| **BR-01** | 입력 행렬은 정확히 4행 4열이다. |
| **BR-02** | `0`은 빈칸이며, 빈칸 개수는 정확히 2이다. |
| **BR-03** | 유효 값은 `0` 또는 `1~16`이다. |
| **BR-04** | `0`을 제외한 모든 값은 격자 내에서 중복될 수 없다. |
| **BR-05** | 첫 번째 빈칸은 row-major(행 우선) 스캔에서 처음 발견되는 `0`의 1-index 좌표이다. |
| **BR-06** | 두 번째 빈칸은 row-major 스캔에서 두 번째로 발견되는 `0`의 1-index 좌표이다. |
| **BR-07** | 누락 숫자는 `1~16` 중 행렬에 없는 정확히 2개이며, `(small, large)` 오름차순으로 정의한다. |
| **BR-08** | 4×4, `n=4` 마방진의 마방진 상수 `MAGIC_CONSTANT`는 `34`이다. |
| **BR-09** | 완성 행렬은 4행, 4열, 주대각선, 반대각선 각각의 합이 `34`와 같아야 마방진이다. |
| **BR-10** | Attempt 1은 `small → (r1,c1)`, `large → (r2,c2)` 순서로 배치한다. |
| **BR-11** | Attempt 2는 Attempt 1 실패 시에만 `large → (r1,c1)`, `small → (r2,c2)` 순서로 배치한다. |
| **BR-12** | 성공 출력은 `int[6]` = `[r1, c1, n1, r2, c2, n2]`이며 좌표는 1-index이다. |

---

## 12. Input / Output Contract

### 12.1 Input Contract

| Field / Item | Type | Rule | Valid Example | Invalid Example | Error Code / Failure Policy |
|---|---|---|---|---|---|
| Matrix | `int[][]` | non-null | 4×4 배열 | `null` | ERR-BND-001 |
| Row count | int | = 4 | 4 rows | 3 rows | ERR-BND-002 |
| Column count | int | each row length = 4 | 4 cols/row | 5 cols in row 2 | ERR-BND-002 |
| Blank cells | int | count of `0` = 2 | two `0`s | zero or three `0`s | ERR-BND-003 |
| Cell value range | int | `0` or `1~16` | `0`, `7`, `16` | `-1`, `17` | ERR-BND-004 |
| Uniqueness | int | non-zero values unique | no dup except `0` | two `8`s | ERR-BND-005 |

### 12.2 Output Contract (Success)

| Field / Item | Type | Rule | Valid Example | Invalid Example | Failure Policy |
|---|---|---|---|---|---|
| Result array | `int[6]` | length = 6 | `[1,2,7,4,3,14]` | length 5 | Boundary contract test fail |
| r1, c1 | int | 1-index, 1~4 | `1`, `2` | `0`, `5` | Boundary contract test fail |
| n1 | int | missing number at first blank in result order | `7` | out of 1~16 | Domain/Control error |
| r2, c2 | int | 1-index, 1~4 | `4`, `3` | `0` | Boundary contract test fail |
| n2 | int | missing number at second blank in result order | `14` | duplicate of n1 | Domain/Control error |
| Order semantics | — | small-first or reverse per FR-05 | Attempt1 success order | swapped when Attempt1 valid | SC-CTL-001/002 fail |

### 12.3 Output Contract (Failure)

| Condition | Error Code | Message Template | Layer |
|---|---|---|---|
| null matrix | ERR-BND-001 | `Input matrix must not be null` | Boundary |
| Not 4×4 | ERR-BND-002 | `Matrix must be 4x4` | Boundary |
| Blank count ≠ 2 | ERR-BND-003 | `Matrix must contain exactly 2 blank cells (0)` | Boundary |
| Value out of range | ERR-BND-004 | `Cell values must be 0 or 1..16` | Boundary |
| Duplicate non-zero | ERR-BND-005 | `Non-zero values must be unique` | Boundary |
| Both attempts fail | ERR-DOM-001 | `No valid magic square combination for the given blanks` | Entity → Control → Boundary |

---

## 13. Error / Failure Policy

**공통 원칙**

- Boundary 입력 검증 실패 시 **Domain Solver(resolver)는 호출되지 않는다.**
- 오류 코드 체계는 **`ERR-BND-*`**, **`ERR-DOM-*`만** 사용한다.
- 외부 노출 방식(본 PRD 확정): **타입드 예외 + error_code 필드**. Boundary/Control 경계에서 호출자에게 전파한다.

| Condition | Error Code | Message | Layer | Domain Resolver Called? | Related AC |
|---|---|---|---|---|---|
| 4×4가 아닌 입력 | ERR-BND-002 | `Matrix must be 4x4` | Boundary | No | FR-01-AC-01 |
| 빈칸 개수 ≠ 2 | ERR-BND-003 | `Matrix must contain exactly 2 blank cells (0)` | Boundary | No | FR-01-AC-02 |
| 값 범위 위반 | ERR-BND-004 | `Cell values must be 0 or 1..16` | Boundary | No | FR-01-AC-03 |
| 0 제외 중복 | ERR-BND-005 | `Non-zero values must be unique` | Boundary | No | FR-01-AC-04 |
| 두 조합 모두 실패 | ERR-DOM-001 | `No valid magic square combination for the given blanks` | Entity (raised) → Control → Boundary | Yes (Solver invoked, returns failure) | FR-05-AC-03 |

**입력 행렬 불변 정책:** 모든 실패·성공 경로에서 원본 입력 행렬은 변경되지 않는다 (`FR-05-AC-06`).

---

## 14. Non-Functional Requirements

| ID | Requirement | Verification |
|---|---|---|
| **NFR-01** | Domain Logic test coverage ≥ 95% | `pytest-cov` entity/control solver tests |
| **NFR-02** | Boundary Validation coverage ≥ 85% | boundary validator + output contract tests |
| **NFR-03** | Deterministic execution: 동일 입력 → 동일 출력 | repeated test runs assert equal |
| **NFR-04** | No input mutation: Solver/Validator는 입력 행렬을 변경하지 않음 | before/after deep equality test |
| **NFR-05** | Performance: 4×4 단일 실행 ≤ 50ms (로컬 dev 기준) | timed integration test |
| **NFR-06** | Maintainability: Boundary/Domain 책임 분리, ECB 의존 방향 준수 | architecture review + import lint |
| **NFR-07** | No unexplained magic numbers: `34`, `4`, `16`, `2`, `6`은 명명 상수로 선언 | code review |
| **NFR-08** | Overall project coverage ≥ 80% (Cursor Rules minimum) | `pytest --cov` gate |

---

## 15. Dual-Track TDD Strategy

### 15.1 Track A — Boundary / UI Contract TDD

| RED Focus | 보호 Contract |
|---|---|
| 4×4 형상 검증 | Input size |
| 빈칸 2개 검증 | BR-02 |
| 값 범위·중복 검증 | BR-03, BR-04 |
| 출력 길이 6, 1-index | BR-12 |
| 검증 실패 시 Solver 미호출 | FR-01 |
| ERR-BND-* 메시지·코드 | Section 13 |

### 15.2 Track B — Domain / Logic TDD

| RED Focus | 보호 Invariant |
|---|---|
| row-major blank discovery | BR-05, BR-06 |
| missing numbers ascending | BR-07 |
| row/col/diagonal sum = 34 | BR-08, BR-09 |
| small-first success | BR-10 |
| reverse success after small-first fail | BR-11 |
| both attempts fail → ERR-DOM-001 | FR-05-AC-03 |

### 15.3 Parallel Progression Rules

1. UI(Boundary) RED와 Logic(Domain) RED를 **분리**하여 작성한다.
2. 각 Track의 GREEN은 **해당 실패 테스트를 통과하는 최소 구현**만 추가한다.
3. REFACTOR는 **양 Track 테스트가 GREEN인 상태에서만** 수행한다.
4. Domain 전체 구현 후 Boundary를 붙이는 순서는 **금지**한다.
5. 테스트 assertion 완화·삭제·skip으로 GREEN을 만드는 행위는 **금지**한다.
6. 권장 병렬 순서: Boundary 입력 RED → Entity Blank/Missing RED → Entity Validator RED → Control Solver RED → Boundary 출력 RED → Integration

---

## 16. Test Plan / QA

### 16.1 Normal Scenarios

| ID | Scenario | Expected |
|---|---|---|
| SC-CTL-001 | small-first 즉시 성공 | `[r1,c1,small,r2,c2,large]` |
| SC-CTL-002 | small-first 실패 후 reverse 성공 | `[r1,c1,large,r2,c2,small]` |

### 16.2 Exception Scenarios

| ID | Scenario | Expected |
|---|---|---|
| SC-BND-002 | 4×4가 아닌 입력 | ERR-BND-002, Solver 미호출 |
| SC-BND-003 | 빈칸 개수 오류 | ERR-BND-003 |
| SC-BND-004 | 값 범위 오류 | ERR-BND-004 |
| SC-BND-005 | 중복 숫자 | ERR-BND-005 |
| SC-CTL-003 | 두 조합 모두 실패 | ERR-DOM-001 |

### 16.3 Boundary Scenarios

| ID | Scenario | Expected |
|---|---|---|
| SC-BND-006 | 반환 배열 길이 | `len(result) == 6` |
| SC-BND-007 | 1-index 좌표 | all coords in `{1,2,3,4}` |
| SC-DOM-BND-001 | 최소값 1 포함 유효 행렬 | no ERR-BND-004 |
| SC-DOM-BND-002 | 최대값 16 포함 유효 행렬 | no ERR-BND-004 |
| SC-DOM-BND-003 | `0`은 빈칸으로만 허용 | exactly 2 zeros pass FR-01 |

### 16.4 Representative Test Data

| ID | Purpose | Matrix (4×4) | Expected |
|---|---|---|---|
| **TD-001** | small-first success | `[0,3,2,13], [5,11,10,8], [9,7,6,12], [4,14,15,0]` | `[1,1,1,4,4,16]` — Attempt 1 valid |
| **TD-002** | reverse success | `[0,14,15,4], [9,7,6,12], [5,11,10,8], [16,2,3,13]` | `[1,1,16,1,2,2]` — Attempt 1 invalid, Attempt 2 valid |
| **TD-003** | invalid size | 3×3 matrix | ERR-BND-002 |
| **TD-004** | invalid blank count | one `0` only in otherwise valid grid | ERR-BND-003 |
| **TD-005** | duplicate value | two `8`s, two blanks | ERR-BND-005 |
| **TD-006** | invalid range | cell value `17` | ERR-BND-004 |
| **TD-007** | both attempts fail | `[1,2,3,4], [5,6,7,8], [9,10,0,12], [13,14,15,0]` | ERR-DOM-001 |

> **Note:** TD-001, TD-002, TD-007은 구현 RED 단계에서 마방진 합·조합 결과를 `pytest`로 재검증한다. PRD 수준에서는 기대 **행동**을 고정하고, 행렬-기대값 쌍은 Scenario ID와 1:1로 유지한다.

### 16.5 Gherkin Summary (Report/05 Level 4)

```gherkin
Feature: Magic Square 4x4 Two-Blank Solver

  Background:
    Given the input is a 4x4 integer matrix
    And 0 represents a blank cell
    And exactly 2 blank cells exist

  Scenario SC-CTL-001: small-first success
    When the solver runs with TD-001
    Then the result equals [1,1,1,4,4,16]

  Scenario SC-CTL-002: reverse success
    When the solver runs with TD-002
    Then the result equals [1,1,16,1,2,2]

  Scenario SC-BND-003: invalid blank count
    When the solver runs with TD-004
    Then ERR-BND-003 is raised
    And the domain solver is not invoked

  Scenario SC-BND-005: duplicate non-zero
    When the solver runs with TD-005
    Then ERR-BND-005 is raised

  Scenario SC-CTL-003: unsolvable
    When the solver runs with TD-007
    Then ERR-DOM-001 is raised
```

---

## 17. Architecture Overview, High-Level

```
[Caller / CLI / Test]
        │
        ▼
┌─────────────────────┐
│  Boundary Layer     │  Input validation, error mapping, output format check
│  BoundaryValidator  │
│  ResultFormatter    │
└─────────┬───────────┘
          │ boundary → control
          ▼
┌─────────────────────┐
│  Control Layer      │  SolveUseCase orchestration
│  Solver (Use Case)  │  Attempt1 → Attempt2
└─────────┬───────────┘
          │ control → entity
          ▼
┌─────────────────────┐
│  Entity Layer       │  Pure domain rules
│  BlankFinder        │
│  MissingNumberFinder│
│  MagicSquareValidator│
└─────────────────────┘
```

**의존 방향**

- 허용: `boundary → control → entity`
- 금지: `boundary → entity` 직접, `entity → control`, `entity → boundary`
- Domain(Entity)은 UI, DB, Web, 파일 시스템, 네트워크에 의존하지 않는다.

---

## 18. Component Candidates

| Component | Responsibility | Layer | Input | Output | Related FR | Related Test |
|---|---|---|---|---|---|---|
| **BoundaryValidator** | 입력 계약 검증, ERR-BND-* | Boundary | `int[][]` | valid matrix or error | FR-01 | SC-BND-002~005 |
| **BlankFinder** | row-major blank coords | Entity | valid `int[4][4]` | `(r1,c1,r2,c2)` 1-index | FR-02 | SC-DOM-001 |
| **MissingNumberFinder** | missing two numbers sorted | Entity | valid matrix | `(small,large)` | FR-03 | SC-DOM-002 |
| **MagicSquareValidator** | magic square boolean check | Entity | full `int[4][4]` | `bool` | FR-04 | SC-DOM-003~005 |
| **Solver** | Attempt1/2 orchestration | Control | valid matrix | `int[6]` or ERR-DOM-001 | FR-05 | SC-CTL-001~003 |
| **ResultFormatter** | output length/index guard | Boundary | `int[6]` | `int[6]` | FR-05 | SC-BND-006~007 |

---

## 19. Risks & Ambiguities

| Risk | Impact | Decision / Mitigation |
|---|---|---|
| 1-index vs 0-index 혼동 | 잘못된 좌표 출력 | BR-05/12, SC-BND-007, 모든 AC에 1-index 명시 |
| row-major 첫 빈칸 정의 누락 | Attempt 순서 오류 | BR-05/06, SC-DOM-001, TD-001/002 분리 |
| small-first vs reverse 데이터 혼동 | 잘못된 GREEN | TD-001(small-first), TD-002(reverse) 별도 ID |
| 입력 행렬 변경 여부 불명확 | 부수효과·회귀 | NFR-04, FR-05-AC-06, 복사본 사용 |
| 두 조합 실패 정책 누락 | Boundary 계약 불일치 | ERR-DOM-001 + UnsolvableCombinationError 확정 |
| 34 상수 하드코딩 | 유지보수·규칙 위반 | `MAGIC_CONSTANT = 34` 명명 상수 |
| Boundary/Domain 책임 혼합 | ECB 위반 | FR별 Layer 분리, FR-05 Control/Entity/Boundary 역할 분리 |
| Report/01 PASS/FAIL 모델과 혼재 | 범위 creep | Out-of-Scope 명시, 본 PRD Solver 계약 우선 |

---

## 20. Engineering Principles

| Principle | Source | Requirement |
|---|---|---|
| ECB layer separation | `.cursor/rules/magicsquare-ecb-architecture.mdc` | boundary/control/entity, 의존 방향 준수 |
| Dual-Track TDD | Report/03, TDD rules | Boundary RED ∥ Domain RED |
| RED-GREEN-REFACTOR | `.cursor/rules/magicsquare-tdd-testing.mdc` | RED 확인 전 구현 금지 |
| pytest + AAA | TDD rules | Arrange-Act-Assert |
| Type hints | code-style rule | 모든 함수 파라미터·반환 타입 |
| PEP 8, line length 88 | code-style rule | Python 3.10+ |
| Coverage ≥ 80% overall | project rule | NFR-08 |
| Domain 95%+, Boundary 85%+ | Report/05 Epic | NFR-01, NFR-02 |
| `print()` 금지 | forbidden rule | logging/debugger 사용 |
| bare `except:` 금지 | forbidden rule | 구체 예외 타입 |
| magic number 금지 | forbidden rule | 명명 상수 |
| 테스트 약화 금지 | TDD rules | assertion/skip/deletion 금지 |
| Package layout | project rule | `MagicSquare/{boundary,control,entity,tests}` |

---

## 21. Traceability Matrix

| Concept / Invariant | Business Rule | Feature ID | Acceptance Criteria | Test Case Candidate | Component |
|---|---|---|---|---|---|
| 4×4 입력 | BR-01 | FR-01 | FR-01-AC-01 | SC-BND-002, TD-003 | BoundaryValidator |
| 빈칸 2개 | BR-02 | FR-01 | FR-01-AC-02 | SC-BND-003, TD-004 | BoundaryValidator |
| 값 범위 0 또는 1~16 | BR-03 | FR-01 | FR-01-AC-03 | SC-BND-004, TD-006 | BoundaryValidator |
| 중복 금지 | BR-04 | FR-01 | FR-01-AC-04 | SC-BND-005, TD-005 | BoundaryValidator |
| row-major 첫 빈칸 | BR-05 | FR-02 | FR-02-AC-01 | SC-DOM-001, TD-001 | BlankFinder |
| row-major 둘째 빈칸 | BR-06 | FR-02 | FR-02-AC-02 | SC-DOM-001, TD-001 | BlankFinder |
| 빈칸 2개 좌표 쌍 | BR-02, BR-05, BR-06 | FR-02 | FR-02-AC-03 | SC-DOM-001 | BlankFinder |
| 누락 숫자 2개 | BR-07 | FR-03 | FR-03-AC-01 | SC-DOM-002 | MissingNumberFinder |
| 누락 숫자 오름차순 | BR-07 | FR-03 | FR-03-AC-02, FR-03-AC-03 | SC-DOM-002, TD-001 | MissingNumberFinder |
| 마방진 상수 34 | BR-08 | FR-04 | FR-04-AC-01 | SC-DOM-003~005 | MagicSquareValidator |
| 행/열/대각선 합 | BR-09 | FR-04 | FR-04-AC-02~04 | SC-DOM-003~005 | MagicSquareValidator |
| small-first 시도 | BR-10 | FR-05 | FR-05-AC-01 | SC-CTL-001, TD-001 | Solver |
| reverse 시도 | BR-11 | FR-05 | FR-05-AC-02 | SC-CTL-002, TD-002 | Solver |
| int[6] 반환 | BR-12 | FR-05 | FR-05-AC-04 | SC-BND-006 | ResultFormatter |
| 1-index 좌표 | BR-12 | FR-05 | FR-05-AC-05 | SC-BND-007, TD-001 | ResultFormatter |
| 입력 불변 | — | FR-05 | FR-05-AC-06 | NFR-04 integration | Solver |
| 두 조합 실패 | — | FR-05 | FR-05-AC-03 | SC-CTL-003, TD-007 | Solver |
| 검증 통과 시만 Solver | — | FR-01 | FR-01-AC-05 | SC-BND-003 mock | BoundaryValidator |

---

## 22. Open Questions / Decision Needed

| ID | Topic | Conflict / Gap | Recommended Resolution |
|---|---|---|---|
| **DN-01** | Report/01 vs Solver PRD | Report/01은 16칸 PASS/FAIL 검증기; 본 PRD는 2빈칸 Solver | **본 PRD Solver 계약을 In-Scope로 확정**. Report/01 검증기는 별도 Epic |
| **DN-02** | `None` 입력 | 고정 계약 본문에 미명시; Report/07 SC-BND-001 존재 | ERR-BND-001 포함 여부 팀 확인 (본 PRD는 포함) |
| **DN-03** | TD-002 행렬·기대값 | reverse 전용 데이터는 RED 단계에서 합 검증 필요 | TD-002를 SC-CTL-002 전용으로 고정, GREEN 전 재검증 |
| **DN-04** | 커버리지 기준 | Cursor Rules 80% vs Epic 95/85% | **Epic 기준(95/85) + overall 80% floor** 동시 적용 (NFR-01/02/08) |
| **DN-05** | CLI vs 테스트-only 진입점 | Boundary “UI” 형태 미확정 | 콘솔 CLI 또는 테스트 fixture 호출 중 하나를 Sprint 0에서 선택 |

**확정 완료 (Open Question 아님)**

- 두 조합 실패: `ERR-DOM-001` + `UnsolvableCombinationError`
- 오류 코드: `ERR-BND-001~005`, `ERR-DOM-001` 단일 체계
- FR-02-AC-02 Traceability: Matrix row “row-major 둘째 빈칸”에 연결

---

## 23. Appendix

### 23.1 참고 문서 목록

| 문서 | PRD 반영 섹션 |
|---|---|
| `Report/01.problem_definition_report.md` | §2 Background, §3 Problem, §4 Why Chain |
| `Report/02.magic_square_prompt_report.md` | Dual-Track 설계 방향 |
| `Report/03.magic_square_cursorrules_workflow_report.md` | §20 Engineering Principles |
| `Report/04.magic_square_rules_non_tdd_report.md` | Cursor Rules 구조 |
| `Report/05.magic_square_level1_to_level5_report.md` | §6 Vision, §8 Journey, §16 Scenarios |
| `Report/06.magic_square_prd_review_report.md` | §13 Error Policy, §21 Traceability, §22 Open Questions |
| `Report/07.magic_square_tdd_readme_todo_report.md` | §13 Error Codes, §16 Scenario IDs |
| `.cursor/rules/magicsquare-*.mdc` | §20, §23.2 |

### 23.2 Cursor Rules 요약

- **ECB:** boundary(I/O) → control(orchestration) → entity(rules); 역방향·捷徑 금지
- **TDD:** RED(실패 확인) → GREEN(최소 구현) → REFACTOR(동작 불변 구조 개선)
- **Forbidden:** `print()`, unexplained magic numbers, bare `except:`
- **Testing:** pytest, AAA, `test_` prefix, 테스트 약화 금지
- **Structure:** `MagicSquare/boundary`, `control`, `entity`, `tests`

### 23.3 대표 Gherkin Scenario 요약

- SC-CTL-001: TD-001 → small-first `[1,1,1,4,4,16]`
- SC-CTL-002: TD-002 → reverse `[1,1,16,1,2,2]`
- SC-BND-003: TD-004 → ERR-BND-003
- SC-BND-005: TD-005 → ERR-BND-005
- SC-CTL-003: TD-007 → ERR-DOM-001

### 23.4 향후 RED Test ID 후보

| Test ID | Track | Scenario | Layer Target |
|---|---|---|---|
| RED-BND-001 | A | null input | BoundaryValidator |
| RED-BND-002 | A | not 4×4 | BoundaryValidator |
| RED-BND-003 | A | blank count | BoundaryValidator |
| RED-BND-004 | A | range | BoundaryValidator |
| RED-BND-005 | A | duplicate | BoundaryValidator |
| RED-BND-006 | A | output length 6 | ResultFormatter |
| RED-BND-007 | A | 1-index coords | ResultFormatter |
| RED-DOM-001 | B | row-major blanks | BlankFinder |
| RED-DOM-002 | B | missing sorted | MissingNumberFinder |
| RED-DOM-003 | B | row sum 34 | MagicSquareValidator |
| RED-DOM-004 | B | col sum 34 | MagicSquareValidator |
| RED-DOM-005 | B | diagonal sum 34 | MagicSquareValidator |
| RED-CTL-001 | B | small-first | Solver |
| RED-CTL-002 | B | reverse | Solver |
| RED-CTL-003 | B | unsolvable | Solver |
| RED-INT-001 | Integration | TD-001 E2E | boundary→control→entity |
| RED-INT-002 | Integration | TD-002 E2E | boundary→control→entity |

---

*문서 버전: PRD v1.0 — 구현·테스트 코드 미포함*
