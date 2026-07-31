# 나만의 퀴즈 게임 🎯

> 터미널에서 동작하는 콘솔 퀴즈 게임
> **Python** (클래스 · 파일 입출력 · 예외 처리) × **Git/GitHub** (브랜치 · 병합 · PR)

외부 라이브러리 없이 표준 라이브러리만 사용한다. 프로그램을 껐다 켜도 추가한 퀴즈와 최고 점수가 유지된다.

---

## 목차

| 장 | 내용 |
|---|---|
| [1. 프로젝트 개요](#1-프로젝트-개요) | 무엇을, 왜 만들었는가 |
| [2. 퀴즈 주제와 선정 이유](#2-퀴즈-주제와-선정-이유) | 주제 선택의 근거 |
| [3. 실행 방법](#3-실행-방법) | 설치 없이 바로 실행 |
| [4. 실행 화면](#4-실행-화면) | 실제 터미널 출력 |
| [5. 기능 목록](#5-기능-목록) | 메뉴 5개와 공통 입력 처리 |
| [6. 프로젝트 구조](#6-프로젝트-구조) | 파일 구성과 모듈 관계 |
| [7. 데이터 파일 (state.json)](#7-데이터-파일-statejson) | 저장 형식과 스키마 |
| [8. 설계 의도](#8-설계-의도) | "왜 이렇게 짰나"에 대한 답 |
| [9. 트러블슈팅](#9-트러블슈팅) | 실제로 막혔던 4가지 |
| [10. 학습 정리](#10-학습-정리) | Python · 클래스 · 파일입출력 · Git |

> 💡 **설명 순서:** 개요(1) → 실행 시연(3·4) → 구조와 설계 의도(6·8) → 트러블슈팅(9) → 개념 정리(10)

---

## 1. 프로젝트 개요

Python 기본 문법, 클래스, 파일 입출력(JSON), Git을 **하나의 동작하는 프로그램**으로 엮는 것이 목표다. 메뉴에서 번호를 고르면 퀴즈 풀기 · 추가 · 목록 · 점수 확인이 동작하고, 종료 후 다시 켜도 데이터가 유지된다(**데이터 영속성**).

핵심은 기능 구현이 아니라 **"왜 이렇게 나눴는가"를 설명할 수 있는 것**이다. 그래서 책임을 셋으로 분리했다.

| 책임 | 담당 |
|---|---|
| 문제 한 개를 표현한다 | `Quiz` ([quiz.py](quiz.py)) |
| 게임 흐름을 제어한다 | `QuizGame` ([quiz_game.py](quiz_game.py)) |
| 파일에 저장/복원한다 | `storage` ([storage.py](storage.py)) |

---

## 2. 퀴즈 주제와 선정 이유

**주제: 기초 컴퓨터·개발 상식** — HTTP 상태 코드, 파이썬 자료형, Git 명령어, 비트/바이트, JSON 구조, 터미널 명령

이 미션 자체가 개발 입문 과정이므로, **게임을 만들면서 그 과정에서 배우는 개념을 문제로 복습**할 수 있도록 골랐다. 기본 문제 6개는 코드에 내장돼 있고([storage.py:20-51](storage.py#L20-L51)), 메뉴 2번으로 추가할 수 있다.

---

## 3. 실행 방법

```bash
git clone https://github.com/JunHyeok-Cha/Codyssey-week2-quizgame.git
cd Codyssey-week2-quizgame
python3 main.py
```

- **환경:** Python 3.10 이상
- **의존성:** 없음 (표준 라이브러리 `json`, `os`만 사용)

첫 실행 시 `state.json`이 없으므로 내장 퀴즈 6개로 시작한다. 퀴즈를 추가하거나 한 판 끝내면 파일이 자동 생성된다.

---

## 4. 실행 화면

**메인 메뉴 / 퀴즈 풀기**

```
📂 저장된 데이터가 없어 기본 퀴즈로 시작합니다.

========================================
        🎯 나만의 퀴즈 게임 🎯
========================================
1. 퀴즈 풀기
2. 퀴즈 추가
3. 퀴즈 목록
4. 점수 확인
5. 종료
========================================
선택: 1

📝 퀴즈를 시작합니다! (총 6문제)

----------------------------------------
[문제 1]
HTTP 상태 코드 404가 의미하는 것은?

  1. 서버 내부 오류
  2. 요청 성공
  3. 찾을 수 없음
  4. 권한 없음
정답 입력 (1-4): 3
✅ 정답입니다!

----------------------------------------
[문제 2]
다음 중 파이썬에서 '변경 불가능(immutable)'한 자료형은?

  1. list
  2. dict
  3. set
  4. tuple
정답 입력 (1-4): 1
❌ 오답입니다. 정답은 4번.

========================================
🏆 결과: 6문제 중 5문제 정답! (83점)
🎉 새로운 최고 점수입니다!
========================================
```

**잘못된 입력 처리** — 어떤 입력에도 죽지 않는다.

```
선택: abc
⚠️ 숫자만 입력할 수 있습니다.
선택: 9
⚠️ 1~5 사이의 숫자를 입력하세요.
선택:
⚠️ 빈 입력입니다. 다시 입력하세요.
선택: 5

👋 게임을 종료합니다. 안녕히 가세요!
```

> 제출용 스크린샷은 [docs/screenshots/](docs/screenshots/)에 보관한다.

---

## 5. 기능 목록

| 메뉴 | 기능 | 설명 | 구현 |
|---|---|---|---|
| 1 | 퀴즈 풀기 | 전체 문제를 순서대로 출제, 정답 수를 100점 만점으로 환산 | [`play()`](quiz_game.py#L67) |
| 2 | 퀴즈 추가 | 문제 · 선택지 4개 · 정답 번호를 입력받아 등록 후 저장 | [`add_quiz()`](quiz_game.py#L102) |
| 3 | 퀴즈 목록 | 등록된 모든 문제를 번호와 함께 표시 | [`list_quizzes()`](quiz_game.py#L129) |
| 4 | 점수 확인 | 저장된 최고 점수 표시 | [`show_score()`](quiz_game.py#L142) |
| 5 | 종료 | 저장 후 안전하게 종료 | [`run()`](quiz_game.py#L159) |

### 공통 입력 처리

숫자를 받는 모든 지점에서 아래를 동일하게 처리한다. 로직은 [`ask_int()`](quiz_game.py#L30) 한 곳에 모았다.

| 상황 | 입력 예 | 동작 |
|---|---|---|
| 앞뒤 공백 | `" 3 "` | `strip()`으로 제거 후 정상 처리 |
| 숫자가 아님 | `abc` | 안내 후 재입력 |
| 범위 밖 | 메뉴에서 `9` | 안내 후 재입력 |
| 빈 입력 | 그냥 Enter | 안내 후 재입력 |
| `Ctrl+C` / `EOF` | – | **저장 후** 안전 종료 (트레이스백 없음) |

---

## 6. 프로젝트 구조

```
Codyssey-week2-quizgame/
├── README.md              # 본 문서
├── .gitignore             # __pycache__, state.json 등 제외
├── main.py                # 진입점 — QuizGame을 만들고 실행만 담당
├── quiz.py                # Quiz 클래스 — 문제 1개 표현 + 정답 판정
├── quiz_game.py           # QuizGame 클래스 — 메뉴 · 흐름 · 입력 처리
├── storage.py             # JSON 저장/불러오기 + 기본 퀴즈 데이터
├── state.json             # 실행 중 자동 생성 (git 제외)
└── docs/screenshots/      # 제출용 스크린샷
```

### 모듈 관계

```
        main.py
           │  QuizGame() 생성 후 run() 호출
           ▼
     ┌─────────────┐   Quiz 객체 생성/사용   ┌──────────┐
     │ quiz_game.py│ ──────────────────────▶ │ quiz.py  │
     │  QuizGame   │                         │  Quiz    │
     └─────────────┘                         └──────────┘
           │  load_state() / save_state()          │
           ▼                                       │ to_dict()
     ┌─────────────┐                               │ from_dict()
     │ storage.py  │ ◀─────────────────────────────┘
     │   JSON I/O  │        (dict ↔ Quiz 변환)
     └─────────────┘
           │
           ▼
      state.json
```

**의존 방향이 한쪽으로만 흐른다.** `quiz.py`와 `storage.py`는 서로를 모르고, `QuizGame`만 둘 다 안다. 그래서 저장 방식을 바꿔도(JSON → DB) `Quiz`는 손댈 필요가 없다.

---

## 7. 데이터 파일 (state.json)

| 항목 | 값 |
|---|---|
| **경로** | 프로젝트 루트의 `state.json` |
| **역할** | 퀴즈 목록과 최고 점수를 종료 후에도 유지 |
| **인코딩** | UTF-8 (`ensure_ascii=False`로 한글 그대로 저장) |
| **생성 시점** | 퀴즈 추가 / 게임 완료 / 종료 시 자동 |

```json
{
  "quizzes": [
    {
      "question": "HTTP 상태 코드 404가 의미하는 것은?",
      "choices": ["서버 내부 오류", "요청 성공", "찾을 수 없음", "권한 없음"],
      "answer": 3
    }
  ],
  "best_score": 83
}
```

| 필드 | 타입 | 의미 |
|---|---|---|
| `quizzes[].question` | 문자열 | 문제 |
| `quizzes[].choices` | 배열(4개) | 선택지 |
| `quizzes[].answer` | 정수(1~4) | 정답 번호 |
| `best_score` | 정수 | 최고 점수 (100점 만점) |

**파일이 없거나 손상된 경우** — 어떤 경우에도 프로그램이 죽지 않는다. ([storage.py:54-96](storage.py#L54-L96))

| 상황 | 동작 |
|---|---|
| 파일 없음 (첫 실행) | 안내 후 내장 퀴즈 6개로 시작 |
| 내용 손상 (JSON 아님 / 키 누락) | 안내 후 기본 퀴즈로 복구 |
| 저장 실패 (권한 등) | 안내만 하고 게임은 계속 진행 |

---

## 8. 설계 의도

### 클래스를 2개로 나눈 이유 — `Quiz` vs `QuizGame`

- **`Quiz`** 는 데이터(문제·선택지·정답)와 **그 데이터에 대한 행동**(정답 판정, 출력)을 묶는다.
- **`QuizGame`** 은 흐름 제어(메뉴·입력·저장)를 맡고, 문제가 어떻게 생겼는지는 `Quiz`에 위임한다.

→ **"정답 판정 방식을 바꾼다" = `Quiz`만**, **"메뉴를 바꾼다" = `QuizGame`만** 손대면 된다. = **단일 책임 원칙(SRP)**

### 저장 로직을 `storage.py`로 뺀 이유

"게임을 어떻게 진행하는가"와 "어떤 파일에 어떤 형식으로 저장하는가"는 별개의 관심사다. 분리해두면 JSON을 DB로 바꿔도 `QuizGame`은 그대로다. = **관심사의 분리(SoC)**

### `to_dict` / `from_dict` 가 필요한 이유

`json` 모듈은 `Quiz` 객체를 저장할 줄 모른다 — 순수 `dict`/`list`/`str`/`int`만 안다. 그래서 **객체와 저장 형식 사이의 다리**를 둔다.

```python
raw = [q.to_dict() for q in self.quizzes]                # 저장: 객체 → dict
self.quizzes = [Quiz.from_dict(q) for q in raw_quizzes]  # 복원: dict → 객체
```

### `ask_int`로 입력 처리를 한 곳에 모은 이유

메뉴 선택 · 정답 입력 · 정답 번호 입력이 모두 "숫자를, 범위 안에서, 안전하게" 받아야 한다. **검증 규칙이 바뀌어도 한 곳만 고치면 세 곳이 반영된다.** = **DRY**

### 정답을 문자열이 아닌 `1~4` 번호로 관리하는 이유

문자열(`"찾을 수 없음"`)로 비교하면 오타 · 띄어쓰기에 취약하다. 번호로 관리하면 비교가 `user_choice == self.answer` 한 줄로 끝나고 화면의 선택지 순서와 직결된다.

---

## 9. 트러블슈팅

### 1. 숫자 입력 검증을 isdigit()에서 try/except로 전환
- **문제:** `raw.lstrip("-").isdigit()`로 숫자 여부를 검사했으나, 음수 부호를 직접 떼어내야 하고 `"²"` 같은 유니코드 숫자 문자는 `isdigit()`가 True를 주지만 `int()`에서는 예외가 발생하는 허점이 있었다.
- **원인 가설:** `isdigit()`는 순수 0~9 문자만 검사해 `int()`가 실제로 변환 가능한 범위와 정확히 일치하지 않는다.
- **해결:** 변환 가능 여부를 직접 판정하는 대신 `int(raw)`를 `try/except ValueError`로 감싸, `int()`가 처리하는 형식을 그대로 검증 기준으로 삼았다.
- **결과:** 부호 처리용 `lstrip("-")` 땜빵이 사라지고, 과제 요구사항인 try/except 예외 처리를 입력 단에서 실제로 활용하게 되었다.

### 2. `Ctrl+C` 시 빨간 에러가 그대로 노출됨

- **원인:** `KeyboardInterrupt` / `EOFError`를 처리하지 않으면 비정상 종료되고 점수도 날아감
- **해결:** 메인 루프를 감싸 **저장 후** 종료

```python
except (KeyboardInterrupt, EOFError):
    print("\n\n⚠️ 입력이 중단되었습니다. 저장 후 종료합니다.")
    self.save()
```

> 예외 처리를 "죽지 않게 하는 것"을 넘어 **"데이터를 잃지 않게 하는 것"** 에 쓴 사례다.

### 3. 로컬 브랜치가 GitHub에 안 보이고, 병합 기록도 안 남음

**증상** — `git checkout -b feature/play`로 작업했는데 GitHub에 브랜치가 없었고, 병합 후에도 Network 그래프에 갈라진 흔적이 없었다.

**원인**
1. `checkout -b`로 만든 브랜치는 **로컬에만** 존재한다. push 전까지 원격에 생기지 않는다.
2. 병합이 **fast-forward**로 처리되면 머지 커밋이 생기지 않아 갈라짐이 기록되지 않는다.

```bash
git branch      # feature/play 보임     → 로컬에는 있다
git branch -r   # feature/play 안 보임  → 원격에는 없다
```

**해결**

```bash
git push -u origin feature/play      # ① 원격에도 만들고 추적 연결

git checkout main                    # ② --no-ff로 머지 커밋 강제
git merge --no-ff feature/play -m "Merge: 퀴즈 풀기 기능 병합"
git push
```

**결과** — GitHub **Insights → Network**에 갈라졌다 합쳐진 선이 표시되고 머지 커밋이 남는다. 로컬에서는 `git log --oneline --graph --all`로 확인한다.

> `checkout` · `pull` · `clone` 수행 증거는 **터미널 스크린샷**으로 남긴다.

---

## 10. 학습 정리

각 개념을 **무엇인가 → 왜 쓰는가 → 이 프로젝트 어디에 쓰였는가** 순서로 정리한다.

- [10.1 Python 기초](#101-python-기초) · [10.2 클래스와 객체](#102-클래스와-객체) · [10.3 파일 입출력](#103-파일-입출력) · [10.4 Git 기초](#104-git-기초)

---

### 10.1 Python 기초

#### 변수

**변수는 값에 붙인 이름표다.** 메모리에 저장된 값을 다시 찾아 쓸 수 있도록 이름을 연결해 둔 것이다.

**왜 쓰는가** — ① 한 번 계산한 값을 재사용하고 ② `100`보다 `best_score`가 의미를 알려주며 ③ 값을 바꿀 때 한 곳만 고치면 된다.

```python
print(3 / 6 * 100)              # 이 3과 6이 무슨 의미인지 알 수 없다

score, total = 3, 6             # 이름 자체가 설명이 된다
points = round(score / total * 100)
print(f"{total}문제 중 {score}문제 정답! ({points}점)")
```

파이썬은 **선언 없이 대입하면 바로 생성**되고 타입도 자동으로 정해진다(동적 타이핑). 그래서 한 변수에는 한 종류의 값만 담는 습관이 중요하다.

> 📌 [quiz_game.py:72-87](quiz_game.py#L72-L87) — `total` · `score` · `points`로 점수 계산을 단계별로 표현했다.

---

#### int, str, bool, list, dict

| 자료형 | 담는 것 | 예시 | 순서 | 변경 | 이 프로젝트에서 |
|---|---|---|---|---|---|
| `int` | 정수 | `42` | – | – | 점수, 정답 번호 |
| `str` | 문자열 | `"안녕"` | 있음 | **불가** | 문제 · 선택지 텍스트 |
| `bool` | 참/거짓 | `True` | – | – | 정답 판정 결과 |
| `list` | **순서 있는** 묶음 | `["A", "B"]` | 있음 | 가능 | 선택지 4개, 퀴즈 목록 |
| `dict` | **키-값** 묶음 | `{"answer": 3}` | 삽입순 | 가능 | 퀴즈 1개, JSON |

```python
score = 3
score += 1                       # int — 계산이 가능하다

question = "1 바이트는 몇 비트인가?"
print("[문제] " + question)       # str — 계산이 아니라 이어붙이기
print("3" + "4")                 # "34"  ← 숫자처럼 보여도 str이면 연결
print(int("3") + int("4"))       # 7     ← 형변환 후 덧셈

is_correct = (score == 4)        # bool — 조건의 결과

choices = ["서버 내부 오류", "요청 성공", "찾을 수 없음", "권한 없음"]
print(choices[0])                # list — 인덱스는 0부터
choices.append("시간 초과")

quiz = {"question": question, "choices": choices, "answer": 3}
print(quiz["question"])          # dict — 이름(키)으로 꺼낸다
print(quiz.get("hint", "없음"))   # 키가 없을 때 기본값 → KeyError 방지
```

**list vs dict** — 순서가 의미를 가지면 `list`(선택지의 1~4번은 정답 번호와 직결), 이름으로 찾아야 하면 `dict`(`quiz[0]`이 뭔지 외울 필요 없이 `quiz["question"]`).

```python
# 실제로는 중첩해서 쓴다 — list 안에 dict, dict 안에 list
quizzes = [{"question": "...", "choices": ["A", "B", "C", "D"], "answer": 3}]
print(quizzes[0]["choices"][2])
```

> 📌 [storage.py:20-51](storage.py#L20-L51)의 `DEFAULT_QUIZZES`가 이 구조(list ⊃ dict ⊃ list)이며, 그대로 JSON이 된다.

---

#### if / elif / else

`if`가 참이면 그 블록만 실행하고 나머지는 건너뛴다. `elif`는 "앞이 거짓일 때 다음 조건", `else`는 "전부 거짓일 때"다.

```python
points = 75

if points >= 90:
    grade = "A"
elif points >= 70:      # 위가 거짓일 때만 검사된다
    grade = "B"
else:
    grade = "C"

print(grade)            # B
```

⚠️ **`elif` 대신 `if`를 연달아 쓰면 의미가 달라진다.** 조건이 독립적으로 모두 검사되어 마지막 참인 것으로 덮어써진다 — 위 예에서 75점인데 `"C"`가 되어버린다.

```python
value, low, high = 3, 1, 4

value == 3                      # 같다 (=는 대입, ==는 비교)
value < low or value > high     # 둘 중 하나라도 참 → 범위 밖
low <= value <= high            # 파이썬은 연결해서 쓸 수 있다
```

> 📌 [quiz_game.py:165-176](quiz_game.py#L165-L176) 메뉴 분기 `if/elif` 체인 · [quiz_game.py:92-94](quiz_game.py#L92-L94) 최고 점수 갱신 판단 · [quiz_game.py:143-146](quiz_game.py#L143-L146) 기록 유무 분기

---

#### for와 while

| | `for` | `while` |
|---|---|---|
| 반복 조건 | **정해진 대상**을 하나씩 순회 | **조건이 참인 동안** 계속 |
| 횟수 | 시작할 때 이미 정해짐 | 실행해 봐야 알 수 있음 |
| 무한루프 위험 | 거의 없음 | **있음** (탈출 조건 필수) |

> **판단 기준: "몇 번 도는지 미리 알 수 있는가?"** 알 수 있으면 `for`, 없으면 `while`.

```python
# for — 대상이 정해져 있다
for quiz in quizzes:
    print(quiz)

for i, quiz in enumerate(quizzes, start=1):   # 번호를 함께 얻는다
    print(f"[문제 {i}] {quiz}")

for n in range(1, 5):                         # 1,2,3,4 (끝 값 미포함)
    print(f"선택지 {n} 입력받기")

# while — 몇 번 물어봐야 할지 모른다
while True:
    raw = input("정답 입력 (1-4): ").strip()
    if not raw.isdigit():
        print("⚠️ 숫자만 입력할 수 있습니다.")
        continue          # 이번 회차를 건너뛰고 처음으로
    if 1 <= int(raw) <= 4:
        break             # 반복문 전체를 종료
    print("⚠️ 1~4 사이의 숫자를 입력하세요.")
```

> 📌 `for` → [quiz_game.py:76](quiz_game.py#L76) 퀴즈 개수만큼 출제(개수를 안다)
> 📌 `while` → [quiz_game.py:36-48](quiz_game.py#L36-L48) `ask_int`(몇 번 틀릴지 모른다), [quiz_game.py:162](quiz_game.py#L162) 메뉴 루프(종료를 고를 때까지)

---

#### 함수

**함수는 "이름 붙인 코드 묶음"이다.**

- **매개변수** — 함수가 받는 입력, 정의할 때 적는 이름
- **인자** — 호출할 때 실제로 넘기는 값
- **반환값** — 돌려주는 결과. `return`이 없으면 `None`

```python
def calculate_points(score, total):     # score, total = 매개변수
    if total == 0:
        return 0
    return round(score / total * 100)   # 반환값

points = calculate_points(3, 6)         # 3, 6 = 인자 → 50


def show(question, index=None):         # 기본값 — index는 생략 가능
    header = f"[문제 {index}]" if index is not None else "[문제]"
    print(header, question)
```

⚠️ **`print`와 `return`은 다르다.** `print`는 화면에 출력만 하고 `None`을 돌려준다. **값을 돌려줘야 다른 계산에 이어 쓸 수 있다.**

```python
x = bad(1, 2)           # print만 하는 함수 → x는 None
y = good(1, 2) * 10     # return하는 함수 → 30
```

**왜 나누는가** — 같은 방어 코드를 세 곳에서 각각 쓰면 세 번 중복된다. 함수로 모으면 **한 번만 고쳐도 세 곳이 고쳐진다.** = DRY

> 📌 [quiz_game.py:30-48](quiz_game.py#L30-L48) `ask_int(prompt, low, high)` — 프롬프트와 범위를 매개변수로 받아 검증된 정수를 반환한다. 호출부 세 곳([:79](quiz_game.py#L79) 정답, [:119](quiz_game.py#L119) 정답 번호, [:164](quiz_game.py#L164) 메뉴)에서 재사용.

---

### 10.2 클래스와 객체

#### 클래스가 무엇이고, 왜 사용하는가

**클래스는 설계도, 객체(인스턴스)는 그 설계도로 찍어낸 실물이다.** 붕어빵 틀이 클래스라면 붕어빵 하나하나가 객체다.

핵심은 **"함께 다니는 데이터와, 그 데이터로 하는 행동을 한 덩어리로 묶는 것"**(캡슐화)이다. dict만 쓰면 이런 문제가 생긴다.

```python
quiz = {"question": "...", "choices": [...], "answer": 3}

print(quiz["anser"])                    # 오타! 실행 전까지 모르고 KeyError
if user_choice == quiz["answer"]: ...   # 정답 판정 로직이 여기저기 흩어진다
```

클래스로 묶으면 이렇게 바뀐다.

```python
class Quiz:
    def __init__(self, question, choices, answer):
        self.question = question          # 속성(attribute)
        self.choices = choices
        self.answer = answer

    def is_correct(self, user_choice):    # 메서드(method)
        return user_choice == self.answer


q = Quiz("1 바이트는 몇 비트인가?", ["4", "8", "16", "32"], 2)
print(q.question)        # 속성 접근 — 오타 나면 AttributeError로 바로 드러난다
print(q.is_correct(2))   # True ← 정답 판정 로직이 Quiz 안에 모여 있다
```

**얻는 것** — ① 퀴즈 관련 로직이 한곳에 모이고(응집) ② 클래스 하나로 객체를 얼마든지 만들며(재사용) ③ 오타가 즉시 에러로 드러난다(안전).

> 📌 [`Quiz`](quiz.py)와 [`QuizGame`](quiz_game.py)으로 나눈 이유는 [8장 설계 의도](#8-설계-의도) 참고.

---

#### `__init__`과 `self`

**`__init__`은 생성자다.** `Quiz(...)`로 객체를 만드는 순간 **자동으로 딱 한 번** 호출되어 초기 속성을 세팅한다. 직접 부르지 않는다.

**`self`는 "지금 이 객체 자신"을 가리킨다.**

```python
q1 = Quiz("문제 A", ["a", "b", "c", "d"], 1)
q2 = Quiz("문제 B", ["a", "b", "c", "d"], 4)

print(q1.question)   # 문제 A
print(q2.question)   # 문제 B  ← 같은 클래스지만 각 객체가 자기 값을 따로 갖는다
```

`q1`을 만들 때 `self`는 `q1`, `q2`를 만들 때는 `q2`다.

⚠️ **`self.` 를 빼면 저장되지 않는다.**

```python
def __init__(self, question):
    question = question       # ❌ 지역 변수 — 함수가 끝나면 사라진다
    self.question = question  # ✅ 객체의 속성 — 계속 남는다
```

**`self`는 자동으로 넘어간다.** 정의할 때는 첫 매개변수로 적지만 호출할 때는 넘기지 않는다.

```python
q.is_correct(2)         # 우리가 쓰는 형태
Quiz.is_correct(q, 2)   # 파이썬 내부에서 실제로 벌어지는 일 (self=q)
```

> 📌 [quiz.py:15-21](quiz.py#L15-L21) — `Quiz.__init__`이 속성을 저장한다.
> 📌 [quiz_game.py:21-24](quiz_game.py#L21-L24) — `QuizGame.__init__`은 **생성 시점에 파일까지 불러온다.** `QuizGame()`만으로 데이터가 복원되므로 [main.py](main.py)는 두 줄이면 된다.

---

#### 속성과 메서드

| | 정의 | 품사 | 예 |
|---|---|---|---|
| **속성** | 객체가 **가진 값** | 명사 | `self.question`, `self.best_score` |
| **메서드** | 객체가 **할 수 있는 행동** | 동사 | `is_correct()`, `show()`, `save()` |

```python
class QuizGame:
    def __init__(self):
        self.quizzes = []        # 속성
        self.best_score = 0

    def add_quiz(self, quiz):    # 메서드
        self.quizzes.append(quiz)

    def play(self):
        picked = self.ask_int("정답 입력 (1-4): ", 1, 4)   # 자기 메서드 호출
        ...
        self.save()

game = QuizGame()
print(len(game.quizzes))    # 속성은 () 없이 접근
game.show_score()           # 메서드는 ()를 붙여 호출
```

**`@staticmethod`** — 객체가 아직 없는 상태에서 호출해야 하는 함수용이다. "dict를 받아 Quiz를 **만들어** 돌려주는" 함수는 만들기 전이라 `self`가 없다.

```python
class Quiz:
    @staticmethod
    def from_dict(data):
        return Quiz(data["question"], data["choices"], data["answer"])

q = Quiz.from_dict({...})   # 인스턴스 없이 '클래스 이름.메서드()'로 호출
```

> 📌 속성 [quiz.py:19-21](quiz.py#L19-L21) · 메서드 [quiz.py:23-35](quiz.py#L23-L35), [quiz_game.py:67-153](quiz_game.py#L67-L153) · 정적 메서드 [quiz.py:48-55](quiz.py#L48-L55)

---

### 10.3 파일 입출력

#### 파일 열기 · 읽기 · 쓰기

변수는 **메모리**에 있어서 프로그램이 끝나면 사라진다. 다음 실행에서도 쓰려면 **디스크의 파일**에 남겨야 한다(**데이터 영속성**). 과정은 **열기 → 읽기/쓰기 → 닫기** 3단계다.

```python
# with를 쓰면 블록을 벗어날 때 close()가 자동 호출된다 (에러가 나도 닫힌다)
with open("memo.txt", "w", encoding="utf-8") as f:
    f.write("안녕하세요\n")

with open("memo.txt", "r", encoding="utf-8") as f:
    text = f.read()
```

| 모드 | 의미 | 파일이 없으면 | 기존 내용 |
|---|---|---|---|
| `"r"` | 읽기 | `FileNotFoundError` | – |
| `"w"` | 쓰기 | 새로 생성 | **전부 지워짐** |
| `"a"` | 이어쓰기 | 새로 생성 | 유지, 뒤에 추가 |

⚠️ **`encoding="utf-8"`은 한글을 다룬다면 반드시 지정한다.** 생략하면 OS 기본 인코딩을 따라가 윈도우(cp949)와 맥/리눅스(utf-8) 사이에서 깨진다.

```python
import os
if not os.path.exists("state.json"):     # 파일 존재 여부 확인
    print("저장된 데이터가 없습니다.")
```

> 📌 [storage.py:69](storage.py#L69)(읽기) · [storage.py:91](storage.py#L91)(쓰기) 둘 다 `with` + `encoding="utf-8"`, [storage.py:63](storage.py#L63)에서 첫 실행 여부를 판단한다.

---

#### JSON

**JSON은 구조를 가진 데이터를 텍스트로 표현하는 표준 형식이다.** 이름에 JavaScript가 들어가지만 언어와 무관하며, 파이썬 표준 라이브러리로 바로 다룬다.

**왜 JSON인가?** 그냥 텍스트로 저장하면 이렇게 된다.

```
HTTP 상태 코드 404가 의미하는 것은?,서버 내부 오류,요청 성공,찾을 수 없음,권한 없음,3
```

문제 안에 쉼표가 들어가면 깨지고, 중첩 구조를 표현할 수 없고, 숫자 `3`인지 문자열 `"3"`인지 구분되지 않고, 다시 읽을 규칙을 직접 만들어야 한다. JSON은 **구조와 타입을 그대로 보존**하고, `json.load()` 한 줄로 복원되며, 사람이 읽을 수 있고, 어디서나 통용되는 표준이다.

| Python | JSON |
|---|---|
| `dict` / `list` | object `{ }` / array `[ ]` |
| `str` / `int`, `float` | string / number |
| `True`, `False` / `None` | `true`, `false` / `null` |

```python
import json

# 파이썬 객체 → JSON 파일
with open("state.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

# JSON 파일 → 파이썬 객체
with open("state.json", "r", encoding="utf-8") as f:
    loaded = json.load(f)

# 문자열 버전 (이름에 s가 붙으면 string 대상)
text = json.dumps(data, ensure_ascii=False)
back = json.loads(text)
```

| 옵션 | 빼면 | 넣으면 |
|---|---|---|
| `ensure_ascii=False` | 한글이 `"\ud55c\uae00"`로 이스케이프 | 한글 그대로 저장 |
| `indent=2` | 전부 한 줄로 붙어 나옴 | 들여쓰기로 읽기 좋음 |

**JSON이 저장하지 못하는 것** — `dict`/`list`/`str`/`int`/`float`/`bool`/`None`만 안다. **`Quiz` 같은 사용자 정의 객체는 저장할 수 없어** 변환하는 다리가 필요하다.

```python
raw = [q.to_dict() for q in self.quizzes]                # 저장: 객체 → dict
self.quizzes = [Quiz.from_dict(q) for q in raw_quizzes]  # 복원: dict → 객체
```

> 📌 [`save_state`](storage.py#L84) · [`load_state`](storage.py#L54)가 파일을 다루고, 변환 다리는 [quiz.py:37-55](quiz.py#L37-L55)에 있다. 저장 형식은 [7장](#7-데이터-파일-statejson) 참고.

---

#### try / except

**예외는 실행 중에 발생하는 오류다.** 처리하지 않으면 트레이스백을 뱉으며 즉시 죽는다.

```python
try:
    number = int(input("숫자: "))     # 오류가 날 수 있는 코드
except ValueError:
    print("⚠️ 숫자가 아닙니다.")       # ValueError가 났을 때
else:
    print(f"입력값: {number}")        # 오류가 안 났을 때만 (선택)
finally:
    print("입력 처리 완료")           # 항상 (선택)
```

| 예외 | 언제 |
|---|---|
| `FileNotFoundError` | 없는 파일을 `"r"`로 열 때 |
| `json.JSONDecodeError` | 내용이 올바른 JSON이 아닐 때 |
| `KeyError` | dict에 없는 키를 꺼낼 때 |
| `ValueError` | `int("abc")`처럼 변환 불가 |
| `OSError` | 권한 없음, 디스크 문제 등 |
| `KeyboardInterrupt` / `EOFError` | `Ctrl+C` / 입력 스트림 종료 |

**여러 예외를 한 번에** — 대응이 같다면 튜플로 묶는다. `as e`로 원인을 함께 출력하면 디버깅이 쉽다.

```python
try:
    with open("state.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    return data["quizzes"], data["best_score"]
except (json.JSONDecodeError, KeyError, OSError) as e:
    print(f"⚠️ 데이터 파일이 손상되어 기본 퀴즈로 복구합니다. ({e})")
    return list(DEFAULT_QUIZZES), 0     # 죽지 않고 기본값으로 복구
```

⚠️ **맨손 `except`는 쓰지 않는다.** 모든 예외를 삼켜서 `Ctrl+C`까지 잡아버리고 무엇이 잘못됐는지 알 수 없다. **잡을 예외를 구체적으로 지정**해 예상 못 한 오류는 드러나게 둔다.

> 📌 [storage.py:68-81](storage.py#L68-L81) 손상된 JSON → 기본 데이터 복구 · [storage.py:90-96](storage.py#L90-L96) 저장 실패해도 게임 계속 · [quiz_game.py:161-180](quiz_game.py#L161-L180) `Ctrl+C`를 잡아 **저장 후** 종료

---

### 10.4 Git 기초

#### Git이 무엇이고 왜 필요한가

**Git은 분산 버전 관리 시스템이다.** 변경 이력을 **스냅샷(커밋)** 단위로 기록하고, 원하는 시점으로 되돌리거나 여러 갈래로 작업하다 합칠 수 있게 해준다. Git 없이 개발하면 `최종.py`, `최종_수정.py`, `최종_진짜최종_v2.py`가 쌓인다.

**해결하는 것** — ① 이력 관리(언제·누가·무엇을·왜) ② 되돌리기 ③ 브랜치로 병렬 작업 ④ 협업 ⑤ 원격 백업

> **Git ≠ GitHub** — Git은 내 컴퓨터에서 도는 **프로그램**, GitHub는 저장소를 올려두는 **웹 서비스**다.

**3개의 영역 + 원격** — Git 명령을 이해하는 핵심 모델이다.

```
   작업 디렉토리        스테이징 영역        로컬 저장소         원격 저장소
   (Working Dir)  ──▶  (Staging Area) ──▶  (Local Repo)  ◀──▶  (GitHub)
      파일 수정           git add            git commit      git push / pull
```

"수정했다"와 "기록으로 남기겠다"를 분리한 것이 Git의 특징이다. 그래서 **여러 파일을 고쳤어도 관련 있는 것만 골라 커밋**할 수 있다.

---

#### 핵심 명령어

| 명령 | 하는 일 | 언제 |
|---|---|---|
| `git init` | 새 저장소 생성 (`.git` 폴더 생성) | 프로젝트 시작 시 1회 |
| `git clone` | 기존 원격 저장소를 이력째 복제 | 저장소를 처음 받아올 때 |
| `git add` | 커밋에 포함할 변경 선택 | 커밋 직전 |
| `git commit` | 스냅샷으로 확정 | 의미 있는 작업 단위마다 |
| `git push` | 로컬 커밋 → 원격 | 커밋 후 공유 · 백업 |
| `git pull` | 원격 커밋 → 로컬 (`fetch`+`merge`) | 작업 시작 전 |
| `git checkout` | 브랜치 / 시점 이동 | 작업 갈래를 바꿀 때 |
| `git status` / `git log` | 상태 / 이력 확인 | 수시로 |

```bash
git init                                    # 저장소 생성
git add .                                   # 모든 변경 스테이징 (파일 지정도 가능)
git commit -m "Feat: 퀴즈 목록 기능 구현"     # 기록으로 확정

git remote add origin <URL>                 # 원격 등록 (최초 1회)
git push -u origin main                     # -u: 추적 연결 (최초 1회)
git push                                    # 이후로는 이것만

git pull                                    # 작업 시작 전 습관적으로
git checkout -b feature/play                # 브랜치 생성 + 이동 (-b = branch)
git clone <URL>                             # 이력·브랜치·origin까지 통째로
```

커밋 메시지는 **무엇을 왜 했는지** 알 수 있게 쓴다. 이 프로젝트는 `Feat:` · `Fix:` · `Docs:` 접두어 관례를 따랐다.

```
e512717 Merge pull request #1 from JunHyeok-Cha/feature/play
69baf6a Feat: state.json 저장/불러오기 구현
6e2bbca Feat: 점수 확인 및 최고점수 갱신
```

**`.gitignore`** — 자동 생성물이나 로컬 데이터는 커밋하지 않는다.

```gitignore
__pycache__/
*.pyc
state.json        # 코드에 기본 퀴즈가 내장돼 있어 없어도 실행됨
.DS_Store
```

> 최신 Git은 역할을 나눈 `git switch`(브랜치 이동)와 `git restore`(파일 복원)를 권장하지만 `checkout`도 그대로 동작한다.

---

#### 브랜치 생성과 병합

**브랜치는 커밋 이력의 갈래다.** main을 건드리지 않고 별도 갈래에서 기능을 만들다 완성되면 합친다. 덕분에 main은 항상 **동작하는 상태**로 유지된다.

```
main          A───B───────────────E (merge)
                   \             /
feature/play        C───────D───┘
```

```bash
git checkout -b feature/play                # 1. 브랜치 생성 + 이동
git add . && git commit -m "Feat: ..."      # 2. 작업하고 커밋
git push -u origin feature/play             # 3. 원격에도 만들고 추적 연결

git checkout main && git pull               # 4. main 최신화
git merge --no-ff feature/play -m "Merge: 퀴즈 풀기 기능 병합"
git push                                    # 5. 병합 결과 반영

git branch -d feature/play                  # 6. 정리 (선택)
git push origin --delete feature/play
```

**`--no-ff`를 쓰는 이유** — main에 새 커밋이 없으면 Git은 포인터만 옮기는 **fast-forward** 병합을 한다. 결과 코드는 같지만 **갈라졌다 합쳐진 흔적이 남지 않는다.** `--no-ff`는 머지 커밋을 강제해 그 기록을 보존한다. → [9장 트러블슈팅 4](#4-로컬-브랜치가-github에-안-보이고-병합-기록도-안-남음)

```bash
git branch -a                       # 로컬(-r은 원격, -a는 전부) 브랜치 목록
git log --oneline --graph --all     # 갈라지고 합쳐진 모양을 그림으로 확인
```

**충돌(conflict)** — 두 브랜치가 **같은 파일의 같은 줄**을 다르게 고쳤을 때 발생한다. 표시를 직접 지우고 최종 코드만 남긴 뒤 `git add` → `git commit` 하면 해결된다.

```python
<<<<<<< HEAD
print("현재 브랜치(main)의 내용")
=======
print("병합하려는 브랜치의 내용")
>>>>>>> feature/play
```

**Pull Request(PR)** — 브랜치를 push한 뒤 GitHub에서 PR을 만들면 병합 전 코드 리뷰를 거칠 수 있고 논의가 영구 보존된다. 실무에서 더 일반적인 방식이다.

> 📌 이 프로젝트는 `feature/play` 브랜치에서 퀴즈 풀기 기능을 구현한 뒤 **PR #1로 main에 병합**했다(커밋 `e512717`).

---

#### clone과 pull

```bash
# 다른 PC에서 이어서 작업하기 — 이력·브랜치·origin이 함께 온다
git clone https://github.com/JunHyeok-Cha/Codyssey-week2-quizgame.git
cd Codyssey-week2-quizgame
python3 main.py

# 협업 중 남의 변경 받아오기
git pull                                # = git fetch + git merge
```

**`fetch`와 `pull`의 차이** — 내 작업이 진행 중일 때는 `fetch`로 먼저 확인하는 편이 안전하다.

```bash
git fetch origin                        # 가져오기만 함 — 내 작업은 그대로
git log HEAD..origin/main --oneline     # 무엇이 새로 왔는지 확인
git merge origin/main                   # 확인 후 직접 합치기
```

**협업 흐름**

```bash
git pull                           # 1. 최신화
git checkout -b feature/새기능      # 2. 브랜치 생성
git add . && git commit -m "..."   # 3. 작업 후 커밋
git push -u origin feature/새기능   # 4. 원격에 올리기
                                   # 5. GitHub에서 PR → 리뷰 → 병합
git checkout main && git pull      # 6. 병합 결과를 로컬에 반영
```

> `checkout` · `pull` · `clone`은 커밋을 만들지 않아 GitHub 이력에 남지 않는다. 증거가 필요하면 터미널 스크린샷으로 남긴다.
