# 나만의 퀴즈 게임 🎯

> 터미널에서 동작하는 콘솔 퀴즈 게임
> **Python** (클래스 · 파일 입출력 · 예외 처리) × **Git/GitHub** (브랜치 · 병합 · PR)

외부 라이브러리 없이 **파이썬 표준 라이브러리만** 사용한다. 프로그램을 껐다 켜도 추가한 퀴즈와 최고 점수가 그대로 남는다.

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
| [9. 트러블슈팅](#9-트러블슈팅) | 실제로 막혔던 4가지와 해결 |
| [10. 학습 정리](#10-학습-정리) | Python · 클래스 · 파일입출력 · Git |

> 💡 **설명 순서 추천:** 개요(1) → 실행 시연(3·4) → 구조와 설계 의도(6·8) → Git 이력과 트러블슈팅(9) → 개념 정리(10)

---

## 1. 프로젝트 개요

Python 기본 문법, 객체 지향(클래스), 파일 입출력(JSON), Git 버전 관리를 **하나의 동작하는 프로그램**으로 엮어 보는 것이 목표다.

메뉴에서 번호를 고르면 퀴즈 풀기 · 추가 · 목록 · 점수 확인이 동작하고, 프로그램을 종료했다 다시 켜도 추가한 퀴즈와 최고 점수가 유지된다(**데이터 영속성**).

핵심 학습 포인트는 기능 구현 자체가 아니라 **"왜 이렇게 나눴는가"를 설명할 수 있는 것**이다. 그래서 책임을 세 갈래로 분리했다.

| 책임 | 담당 |
|---|---|
| 문제 한 개를 표현한다 | `Quiz` ([quiz.py](quiz.py)) |
| 게임 흐름을 제어한다 | `QuizGame` ([quiz_game.py](quiz_game.py)) |
| 파일에 저장/복원한다 | `storage` ([storage.py](storage.py)) |

---

## 2. 퀴즈 주제와 선정 이유

**주제: 기초 컴퓨터·개발 상식** — HTTP 상태 코드, 파이썬 자료형, Git 명령어, 비트/바이트, JSON 구조, 터미널 명령

이 미션 자체가 개발 입문 과정이므로, **게임을 만들면서 동시에 그 과정에서 배우는 개념을 문제로 복습**할 수 있도록 주제를 골랐다. 퀴즈를 한 판 풀 때마다 미션의 핵심 용어를 다시 마주치게 된다.

기본 문제는 6개가 코드에 내장돼 있고([storage.py:20-51](storage.py#L20-L51)), 메뉴 2번으로 얼마든지 추가할 수 있다.

---

## 3. 실행 방법

```bash
git clone https://github.com/JunHyeok-Cha/Codyssey-week2-quizgame.git
cd Codyssey-week2-quizgame
python3 main.py
```

- **필요 환경:** Python 3.10 이상
- **의존성:** 없음 (표준 라이브러리 `json`, `os`만 사용)

첫 실행 시에는 `state.json`이 없으므로 코드에 내장된 **기본 퀴즈 6개**로 시작한다. 퀴즈를 추가하거나 게임을 한 판 끝내면 `state.json`이 자동으로 생성된다.

---

## 4. 실행 화면

**메인 메뉴**

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
선택:
```

**퀴즈 풀기 (메뉴 1)**

```
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

**퀴즈 목록 (메뉴 3)**

```
📋 등록된 퀴즈 목록 (총 6개)
----------------------------------------
[1] HTTP 상태 코드 404가 의미하는 것은?
[2] 다음 중 파이썬에서 '변경 불가능(immutable)'한 자료형은?
[3] Git에서 변경 이력을 기록으로 확정하는 명령은?
[4] 1 바이트(byte)는 몇 비트(bit)인가?
[5] JSON에서 데이터를 담는 두 가지 기본 구조는?
[6] 터미널에서 현재 위치(디렉토리)를 출력하는 명령은?
----------------------------------------
```

**잘못된 입력 처리**

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

> 제출용 스크린샷은 [docs/screenshots/](docs/screenshots/)에 보관한다 (menu / play / add_quiz / score).

---

## 5. 기능 목록

| 메뉴 | 기능 | 설명 | 구현 |
|---|---|---|---|
| 1 | 퀴즈 풀기 | 전체 문제를 순서대로 출제하고, 정답 수를 100점 만점으로 환산 | [`play()`](quiz_game.py#L67) |
| 2 | 퀴즈 추가 | 문제 · 선택지 4개 · 정답 번호를 입력받아 등록 후 즉시 저장 | [`add_quiz()`](quiz_game.py#L102) |
| 3 | 퀴즈 목록 | 등록된 모든 문제를 번호와 함께 표시 | [`list_quizzes()`](quiz_game.py#L129) |
| 4 | 점수 확인 | 저장된 최고 점수 표시 (기록이 없으면 안내) | [`show_score()`](quiz_game.py#L142) |
| 5 | 종료 | 저장 후 안전하게 종료 | [`run()`](quiz_game.py#L159) |

### 공통 입력 처리

숫자를 입력받는 **모든 지점**에서 아래를 동일하게 처리한다. 로직은 [`ask_int()`](quiz_game.py#L30) 한 곳에 모아 재사용한다.

| 상황 | 입력 예 | 동작 |
|---|---|---|
| 앞뒤 공백 | `" 3 "` | `strip()`으로 제거 후 정상 처리 |
| 숫자가 아님 | `abc` | 안내 후 재입력 |
| 범위 밖 | 메뉴에서 `9` | 안내 후 재입력 |
| 빈 입력 | 그냥 Enter | 안내 후 재입력 |
| 강제 종료 | `Ctrl+C` | **저장 후** 안전 종료 (트레이스백 없음) |
| 입력 종료 | `EOF` (파이프 종료) | **저장 후** 안전 종료 |

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
├── state.json             # 실행 중 자동 생성되는 데이터 파일 (git 제외)
└── docs/
    └── screenshots/       # 제출용 스크린샷
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
| **역할** | 퀴즈 목록과 최고 점수를 프로그램 종료 후에도 유지 |
| **인코딩** | UTF-8 (`ensure_ascii=False`로 한글이 그대로 저장됨) |
| **생성 시점** | 퀴즈 추가 / 게임 완료 / 종료 시 자동 |

### 스키마

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
| `quizzes` | 배열 | 퀴즈 객체들의 목록 |
| `quizzes[].question` | 문자열 | 문제 |
| `quizzes[].choices` | 배열(4개) | 선택지 |
| `quizzes[].answer` | 정수(1~4) | 정답 번호 |
| `best_score` | 정수 | 최고 점수 (100점 만점) |

### 파일이 없거나 손상된 경우

| 상황 | 동작 |
|---|---|
| 파일 없음 (첫 실행) | `📂 저장된 데이터가 없어 기본 퀴즈로 시작합니다.` → 내장 퀴즈 6개로 시작 |
| 내용 손상 (JSON 아님 / 키 누락) | `⚠️ 데이터 파일이 손상되어 기본 퀴즈로 복구합니다.` → 기본 퀴즈로 복구 |
| 저장 실패 (권한 등) | `⚠️ 저장에 실패했습니다.` → 안내만 하고 게임은 계속 진행 |

어떤 경우에도 프로그램이 죽지 않는다. 구현은 [storage.py:54-96](storage.py#L54-L96) 참고.

---

## 8. 설계 의도

동료평가에서 "왜 이렇게 짰나"를 묻는다면 아래를 근거로 설명한다.

### 클래스를 2개로 나눈 이유 — `Quiz` vs `QuizGame`

- **`Quiz`** 는 데이터(문제·선택지·정답)와 **그 데이터에 대한 행동**(정답 판정, 출력)을 한 덩어리로 묶는다. 문제 하나에 관한 로직이 여기저기 흩어지지 않는다.
- **`QuizGame`** 은 흐름 제어(메뉴·입력·저장)를 맡는다. 문제가 어떻게 생겼는지는 `Quiz`에 위임한다.

이렇게 나누면 **"정답 판정 방식을 바꾼다" → `Quiz`만**, **"메뉴를 바꾼다" → `QuizGame`만** 손대면 된다. = **단일 책임 원칙(SRP)**

### 저장 로직을 `storage.py`로 뺀 이유

"게임을 어떻게 진행하는가"와 "어떤 파일에 어떤 형식으로 저장하는가"는 별개의 관심사다. 분리해두면 저장 방식을 JSON에서 DB로 바꿔도 `QuizGame` 코드는 그대로다. = **관심사의 분리(SoC)**

### `to_dict` / `from_dict` 가 필요한 이유

`json` 모듈은 `Quiz` 객체를 저장할 줄 모른다 — 순수 `dict`/`list`/`str`/`int`만 안다. 그래서 저장 직전에 **객체→dict**(`to_dict`), 불러온 직후에 **dict→객체**(`from_dict`)로 변환한다. **객체와 저장 형식 사이의 다리** 역할이다.

```python
raw = [q.to_dict() for q in self.quizzes]              # 저장할 때
self.quizzes = [Quiz.from_dict(q) for q in raw_quizzes]  # 불러올 때
```

### `ask_int`로 입력 처리를 한 곳에 모은 이유

메뉴 선택 · 정답 입력 · 정답 번호 입력이 모두 "숫자를, 범위 안에서, 안전하게" 받아야 한다. 같은 방어 코드를 세 번 쓰는 대신 함수 하나로 재사용한다. **입력 검증 규칙이 바뀌어도 한 곳만 고치면 세 곳이 모두 반영된다.** = **중복 제거(DRY)**

### 정답을 문자열이 아닌 `1~4` 번호로 관리하는 이유

정답을 문자열(`"찾을 수 없음"`)로 비교하면 **오타 · 띄어쓰기 · 앞뒤 공백**에 취약하다. 번호로 관리하면 비교가 `user_choice == self.answer` 한 줄로 끝나고, 화면에 표시되는 선택지 순서와 직결된다.

### `main.py`를 얇게 유지한 이유

`main.py`는 '시작 버튼' 역할만 한다. 실제 로직은 전부 `QuizGame`에 있다. 나중에 다른 방식으로 게임을 실행하고 싶을 때(예: 테스트 코드) `QuizGame`만 가져다 쓰면 된다.

```python
def main():
    game = QuizGame()   # 생성자에서 데이터 불러오기까지 완료
    game.run()          # 메뉴 루프 시작
```

---

## 9. 트러블슈팅

### 1. 한글이 `state.json`에 `\uXXXX`로 깨져 저장됨

| | |
|---|---|
| **증상** | 저장된 파일을 열어보니 한글이 `"\ud55c\uae00"` 형태로 보임 |
| **원인** | `json.dump`의 기본값 `ensure_ascii=True`가 비ASCII 문자를 이스케이프함 |
| **해결** | `ensure_ascii=False` 옵션 추가 → 한글이 그대로 저장됨 |

```python
json.dump(data, f, ensure_ascii=False, indent=2)
```

### 2. 파일이 깨지면 프로그램이 죽음

| | |
|---|---|
| **증상** | `state.json`을 손으로 수정해 망가뜨리자 실행 즉시 트레이스백 출력 후 종료 |
| **원인** | 손상된 JSON을 `json.load` 하면 `JSONDecodeError` 발생 |
| **해결** | `try/except`로 `JSONDecodeError` · `KeyError` · `OSError`를 잡아 기본 퀴즈로 복구 |

```python
except (json.JSONDecodeError, KeyError, OSError) as e:
    print(f"⚠️ 데이터 파일이 손상되어 기본 퀴즈로 복구합니다. ({e})")
    return list(DEFAULT_QUIZZES), 0
```

### 3. `Ctrl+C` 시 빨간 에러가 그대로 노출됨

| | |
|---|---|
| **증상** | 게임 중 `Ctrl+C`를 누르면 트레이스백이 출력되고, 그때까지의 점수도 저장되지 않음 |
| **원인** | `KeyboardInterrupt` / `EOFError`를 처리하지 않으면 파이썬이 비정상 종료 |
| **해결** | 메인 루프를 `try/except`로 감싸 **저장 후** 안전 종료 |

```python
except (KeyboardInterrupt, EOFError):
    print("\n\n⚠️ 입력이 중단되었습니다. 저장 후 종료합니다.")
    self.save()
```

> 예외 처리를 "죽지 않게 하는 것"을 넘어 **"데이터를 잃지 않게 하는 것"** 에 쓴 사례다.

### 4. 로컬 브랜치가 GitHub에 안 보이고, 병합 기록도 안 남음

| | |
|---|---|
| **증상** | `git checkout -b feature/play`로 브랜치를 만들어 작업했는데 GitHub에는 브랜치가 보이지 않았고, main에 병합한 뒤에도 Network 그래프에 갈라진 흔적이 없었다 |
| **원인 ①** | `checkout -b`로 만든 브랜치는 **로컬에만** 존재한다. push하기 전까지 원격에 생성되지 않는다 |
| **원인 ②** | 병합이 **fast-forward**로 처리되면 머지 커밋이 생기지 않아 그래프에 갈라짐이 기록되지 않는다 |

**확인 방법**

```bash
git branch      # feature/play 가 보임      → 로컬에는 있다
git branch -r   # feature/play 가 안 보임   → 원격에는 없다
```

**해결 ① — 브랜치를 원격에도 만들고 추적 연결한다**

```bash
git push -u origin feature/play
```

이후 그 브랜치에서는 `git push` / `git pull`만 쳐도 원격의 같은 브랜치로 오간다.

**해결 ② — `--no-ff`로 머지 커밋을 강제해 병합 흔적을 남긴다**

```bash
git checkout main
git merge --no-ff feature/play -m "Merge: 퀴즈 풀기 기능 병합"
git push
```

**결과 확인**

- GitHub **Insights → Network** 그래프에 브랜치가 갈라졌다 합쳐진 선이 표시된다
- 커밋 목록에 머지 커밋이 남는다
- 로컬에서는 `git log --oneline --graph --all`로 동일한 이력을 확인할 수 있다

> **비고:** `checkout` · `pull` · `clone`은 "가져오거나 이동하는" 동작이라 커밋을 만들지 않으므로 GitHub 이력에 남지 않는다. 수행 증거는 **터미널 스크린샷**으로 남긴다. 병합 기록을 가장 뚜렷하게 남기려면 브랜치를 push한 뒤 GitHub에서 **Pull Request로 병합**하면 Pull requests 탭에도 이력이 보존된다.

---

## 10. 학습 정리

이번 미션의 학습 목표를 항목별로 정리한다. 각 개념은 **무엇인가 → 왜 쓰는가 → 이 프로젝트 어디에 쓰였는가** 순서로 설명한다.

- [10.1 Python 기초](#101-python-기초) — 변수 · 자료형 · 조건문 · 반복문 · 함수
- [10.2 클래스와 객체](#102-클래스와-객체) — 클래스 · `__init__` · `self` · 속성 · 메서드
- [10.3 파일 입출력](#103-파일-입출력) — 파일 열기/읽기/쓰기 · JSON · `try/except`
- [10.4 Git 기초](#104-git-기초) — 버전 관리 · 핵심 명령 7개 · 브랜치와 병합

---

### 10.1 Python 기초

#### 변수가 무엇이고, 왜 사용하는가

**변수는 값에 붙인 이름표다.** 정확히는, 메모리에 저장된 값을 다시 찾아 쓸 수 있도록 이름을 연결해 둔 것이다.

**왜 쓰는가?** 세 가지 이유가 있다.

1. **재사용** — 한 번 계산한 값을 여러 곳에서 다시 쓸 수 있다
2. **의미 부여** — `100`보다 `best_score`가 무슨 값인지 바로 알려준다. 코드가 곧 설명이 된다
3. **변경 용이** — 값을 바꿀 때 변수를 정의한 한 곳만 고치면 된다

```python
# 변수 없이 — 이 3과 6이 무슨 의미인지 알 수 없고, 바꾸려면 전부 찾아야 한다
print(3 / 6 * 100)

# 변수를 쓰면 — 이름 자체가 설명이 되고, 값 변경도 한 곳에서 끝난다
score = 3          # 맞힌 문제 수
total = 6          # 전체 문제 수
points = round(score / total * 100)
print(f"{total}문제 중 {score}문제 정답! ({points}점)")
# → 6문제 중 3문제 정답! (50점)
```

파이썬에서 변수는 **선언 없이 대입하면 바로 생성**되고, 타입도 자동으로 정해진다.

```python
score = 0          # int로 시작
score = "만점"      # 나중에 str을 넣어도 에러가 아니다 (동적 타이핑)
```

편리하지만 그래서 **한 변수에는 한 종류의 값만 담는 습관**이 중요하다.

> 📌 **이 프로젝트에서:** [quiz_game.py:72-87](quiz_game.py#L72-L87) — `total` · `score` · `points` 변수로 점수 계산 과정을 단계별로 표현했다.

---

#### int, str, bool, list, dict의 차이

| 자료형 | 무엇을 담는가 | 예시 | 순서 | 변경 | 이 프로젝트에서의 쓰임 |
|---|---|---|---|---|---|
| `int` | 정수 | `42`, `-7` | – | – | 점수, 정답 번호 |
| `str` | 문자열(텍스트) | `"안녕"` | 있음 | **불가** | 문제 · 선택지 텍스트 |
| `bool` | 참 / 거짓 | `True`, `False` | – | – | 정답 판정 결과 |
| `list` | 여러 값의 **순서 있는** 묶음 | `["A", "B"]` | 있음 | 가능 | 선택지 4개, 퀴즈 목록 |
| `dict` | **키-값** 쌍의 묶음 | `{"answer": 3}` | 삽입순 | 가능 | 퀴즈 1개, JSON 데이터 |

```python
# int — 계산이 가능한 수
score = 3
score += 1                      # 4

# str — 텍스트. 계산이 아니라 '이어붙이기'가 된다
question = "1 바이트는 몇 비트인가?"
print("[문제] " + question)      # 문자열 + 문자열 = 이어붙이기
print(len(question))             # 글자 수

# 주의: 숫자처럼 보여도 str이면 계산이 아니라 이어붙이기가 된다
print("3" + "4")                 # "34"  ← 문자열 연결
print(int("3") + int("4"))       # 7     ← 형변환 후 덧셈

# bool — 조건의 결과. if와 함께 쓰인다
is_correct = (score == 4)        # True

# list — 순서가 있고, 번호(인덱스)로 꺼낸다. 인덱스는 0부터
choices = ["서버 내부 오류", "요청 성공", "찾을 수 없음", "권한 없음"]
print(choices[0])                # 서버 내부 오류  ← 첫 번째는 0번
print(len(choices))              # 4
choices.append("시간 초과")       # 뒤에 추가 (변경 가능)

# dict — 순서가 아니라 '이름(키)'으로 꺼낸다
quiz = {
    "question": "HTTP 상태 코드 404가 의미하는 것은?",
    "choices": choices,
    "answer": 3,
}
print(quiz["question"])          # 키로 접근
print(quiz.get("hint", "없음"))   # 키가 없을 때 기본값 → 없음 (KeyError 방지)
```

**list vs dict — 언제 무엇을 쓰는가**

- **순서가 의미를 가지면 `list`** — 선택지는 "1번, 2번, 3번, 4번"이라는 순서 자체가 정답 번호와 직결된다
- **이름으로 찾아야 하면 `dict`** — 퀴즈 한 개는 "문제 / 선택지 / 정답"이라는 성격이 다른 값을 묶는다. `quiz[0]`이 문제인지 정답인지 외울 필요 없이 `quiz["question"]`으로 읽는다

```python
# 실제로는 이렇게 중첩해서 쓴다 — list 안에 dict, dict 안에 list
quizzes = [
    {"question": "...", "choices": ["A", "B", "C", "D"], "answer": 3},
    {"question": "...", "choices": ["A", "B", "C", "D"], "answer": 1},
]
print(quizzes[0]["choices"][2])   # 첫 번째 퀴즈의 3번째 선택지
```

> 📌 **이 프로젝트에서:** [storage.py:20-51](storage.py#L20-L51)의 `DEFAULT_QUIZZES`가 정확히 이 구조(list ⊃ dict ⊃ list)이며, 그대로 JSON 파일이 된다.

---

#### if / elif / else — 조건에 따른 분기

**조건에 따라 다른 코드를 실행**하는 문법이다. `if`가 참이면 그 블록만 실행하고 나머지는 건너뛴다. `elif`는 "앞이 거짓일 때 다음 조건", `else`는 "전부 거짓일 때"다.

```python
points = 75

if points >= 90:
    grade = "A"
elif points >= 70:      # 위가 거짓일 때만 검사된다
    grade = "B"
elif points >= 50:
    grade = "C"
else:                   # 어떤 조건도 맞지 않을 때
    grade = "D"

print(grade)            # B
```

**⚠️ `elif` 대신 `if`를 연달아 쓰면 의미가 달라진다**

```python
# 잘못된 예 — 조건이 독립적으로 모두 검사되어 grade가 계속 덮어써진다
if points >= 90: grade = "A"
if points >= 70: grade = "B"
if points >= 50: grade = "C"    # 75점인데 최종 결과가 "C"가 되어버린다
```

**비교 · 논리 연산자**

```python
value, low, high = 3, 1, 4

value == 3                      # 같다 (=는 대입, ==는 비교 — 헷갈리기 쉽다)
value != 3                      # 다르다
value < low or value > high     # 둘 중 하나라도 참 → 범위 밖
low <= value <= high            # 파이썬은 이렇게 연결해서 쓸 수 있다
not (value == 3)                # 부정
```

> 📌 **이 프로젝트에서:**
> - [quiz_game.py:165-176](quiz_game.py#L165-L176) — 메뉴 번호 1~5에 따라 다른 기능을 호출하는 `if/elif` 체인
> - [quiz_game.py:92-94](quiz_game.py#L92-L94) — `if points > self.best_score:` 로 최고 점수 갱신 판단
> - [quiz_game.py:143-146](quiz_game.py#L143-L146) — 기록 유무(`best_score == 0`)에 따른 `if/else` 분기

---

#### for와 while의 차이, 그리고 선택 기준

| | `for` | `while` |
|---|---|---|
| 반복 조건 | **정해진 대상**을 하나씩 순회 | **조건이 참인 동안** 계속 |
| 횟수 | 시작할 때 이미 정해져 있음 | 실행해 봐야 알 수 있음 |
| 대표 상황 | 리스트의 모든 원소 처리 | 올바른 입력을 받을 때까지 |
| 무한루프 위험 | 거의 없음 | **있음** (탈출 조건 필수) |

> **핵심 판단 기준: "몇 번 도는지 미리 알 수 있는가?"**
> 알 수 있으면 `for`, 없으면 `while`.

```python
# for — 대상이 정해져 있다: 퀴즈 6개를 순서대로 출제
quizzes = ["문제1", "문제2", "문제3"]
for quiz in quizzes:
    print(quiz)

# enumerate — 번호를 함께 얻는다. start=1이면 1번부터
for i, quiz in enumerate(quizzes, start=1):
    print(f"[문제 {i}] {quiz}")

# range — 정해진 횟수만큼. range(1, 5)는 1,2,3,4 (끝 값 미포함)
for n in range(1, 5):
    print(f"선택지 {n} 입력받기")
```

```python
# while — 몇 번 물어봐야 할지 모른다: 올바로 입력할 때까지 반복
while True:
    raw = input("정답 입력 (1-4): ").strip()
    if not raw.isdigit():
        print("⚠️ 숫자만 입력할 수 있습니다.")
        continue          # 이번 회차를 건너뛰고 루프의 처음으로
    value = int(raw)
    if 1 <= value <= 4:
        break             # 조건을 만족했으니 루프 전체를 종료
    print("⚠️ 1~4 사이의 숫자를 입력하세요.")
```

- `continue` — 이번 회차를 건너뛰고 **다음 반복으로**
- `break` — 반복문 **전체를 즉시 종료**

> 📌 **이 프로젝트에서:**
> - `for` → [quiz_game.py:76](quiz_game.py#L76) — 퀴즈 개수만큼 출제 (개수를 미리 알 수 있다)
> - `while` → [quiz_game.py:36-48](quiz_game.py#L36-L48) `ask_int` — 사용자가 몇 번 잘못 입력할지 알 수 없다
> - `while` → [quiz_game.py:162](quiz_game.py#L162) — 메뉴 루프. "종료를 고를 때까지" 돌아야 하므로 횟수를 알 수 없다

---

#### 함수 — 정의, 매개변수, 반환값

**함수는 "이름 붙인 코드 묶음"이다.** 같은 일을 여러 번 하거나, 긴 코드를 의미 단위로 쪼갤 때 쓴다.

| 용어 | 뜻 |
|---|---|
| **매개변수(parameter)** | 함수가 받는 입력. 정의할 때 적는 이름 |
| **인자(argument)** | 호출할 때 실제로 넘기는 값 |
| **반환값(return)** | 함수가 돌려주는 결과. `return`이 없으면 `None` |

```python
def calculate_points(score, total):     # score, total = 매개변수
    """맞힌 개수를 100점 만점으로 환산해 돌려준다."""
    if total == 0:                      # 0으로 나누기 방어
        return 0
    return round(score / total * 100)   # 반환값

points = calculate_points(3, 6)         # 3, 6 = 인자
print(points)                           # 50
```

**기본값(default) 매개변수** — 인자를 생략하면 기본값이 쓰인다.

```python
def show(question, index=None):         # index는 생략 가능
    header = f"[문제 {index}]" if index is not None else "[문제]"
    print(header, question)

show("1 바이트는 몇 비트?")             # [문제] 1 바이트는 몇 비트?
show("1 바이트는 몇 비트?", index=3)    # [문제 3] 1 바이트는 몇 비트?
```

**⚠️ `print`와 `return`은 전혀 다르다** — 가장 많이 혼동하는 부분이다.

```python
def bad(a, b):
    print(a + b)        # 화면에 출력만 하고 값을 돌려주지 않는다

def good(a, b):
    return a + b        # 값을 돌려준다 → 다른 계산에 이어 쓸 수 있다

x = bad(1, 2)           # 3이 출력되지만 x는 None
y = good(1, 2) * 10     # 30 — 반환값이 있어야 이런 활용이 가능하다
```

**함수로 나누면 좋은 이유** — 같은 방어 코드(공백 제거 → 숫자 확인 → 범위 확인)를 세 곳에서 각각 쓰면 세 번 중복된다. 함수 하나로 모으면 **한 번만 고쳐도 세 곳이 모두 고쳐진다.** = DRY(Don't Repeat Yourself)

> 📌 **이 프로젝트에서:** [quiz_game.py:30-48](quiz_game.py#L30-L48)의 `ask_int(prompt, low, high)` — 프롬프트 문구와 허용 범위를 매개변수로 받아 **검증된 정수를 반환**한다. 호출부 세 곳([:79](quiz_game.py#L79) 정답 입력, [:119](quiz_game.py#L119) 정답 번호, [:164](quiz_game.py#L164) 메뉴 선택)에서 재사용된다.

---

### 10.2 클래스와 객체

#### 클래스가 무엇이고, 왜 사용하는가

**클래스는 설계도, 객체(인스턴스)는 그 설계도로 찍어낸 실물이다.** 붕어빵 틀이 클래스라면 붕어빵 하나하나가 객체다.

**왜 쓰는가?** 핵심은 **"함께 다니는 데이터와, 그 데이터로 하는 행동을 한 덩어리로 묶는 것"**(캡슐화)이다.

dict만으로 퀴즈를 다루면 이런 문제가 생긴다.

```python
# dict 방식 — 동작은 하지만 불편하다
quiz = {"question": "...", "choices": [...], "answer": 3}

print(quiz["anser"])                    # 오타! 실행 전까지 모르고, 터지면 KeyError
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
        """이 퀴즈의 정답인지 판정한다."""
        return user_choice == self.answer


# 객체(인스턴스) 만들기 — 클래스 이름을 함수처럼 호출한다
q = Quiz("1 바이트는 몇 비트인가?", ["4", "8", "16", "32"], 2)

print(q.question)        # 속성 접근 — 오타 나면 AttributeError로 바로 드러난다
print(q.is_correct(2))   # True  ← 정답 판정 로직이 Quiz 안에 모여 있다
print(q.is_correct(3))   # False
```

**얻는 것**

1. **응집** — 퀴즈에 관한 로직이 `Quiz` 안에 모인다. "정답 판정 방식을 바꾸자"면 이 클래스만 고친다
2. **재사용** — 퀴즈가 100개여도 클래스 하나로 100개의 독립된 객체를 만든다
3. **안전** — `q.anser`처럼 없는 속성에 접근하면 즉시 에러가 나서 오타를 빨리 발견한다

> 📌 **이 프로젝트에서:** 문제 1개를 표현하는 [`Quiz`](quiz.py), 게임 흐름을 담당하는 [`QuizGame`](quiz_game.py). 두 개로 나눈 이유는 [8장 설계 의도](#8-설계-의도) 참고.

---

#### `__init__` 메서드와 `self`의 역할

**`__init__`은 생성자(constructor)다.** `Quiz(...)`로 객체를 만드는 순간 **자동으로 딱 한 번** 호출되며, 그 객체의 초기 상태(속성)를 세팅한다. 직접 `q.__init__()`이라고 부르지 않는다.

**`self`는 "지금 이 객체 자신"을 가리킨다.**

```python
class Quiz:
    def __init__(self, question, choices, answer):
        self.question = question    # ← 이 객체의 question 속성에 저장
        self.choices = choices
        self.answer = answer

q1 = Quiz("문제 A", ["a", "b", "c", "d"], 1)
q2 = Quiz("문제 B", ["a", "b", "c", "d"], 4)

print(q1.question)   # 문제 A
print(q2.question)   # 문제 B  ← 같은 클래스지만 각 객체가 자기 값을 따로 갖는다
```

`q1`을 만들 때 `self`는 `q1`이고, `q2`를 만들 때 `self`는 `q2`다.

**⚠️ `self.` 없이 그냥 `question = question`이라고 쓰면 저장되지 않는다**

```python
def __init__(self, question):
    question = question       # ❌ 지역 변수에 대입 — 함수가 끝나면 사라진다
    self.question = question  # ✅ 객체의 속성으로 저장 — 계속 남는다
```

**`self`는 자동으로 넘어간다.** 메서드를 정의할 때는 첫 번째 매개변수로 반드시 `self`를 적지만, 호출할 때는 넘기지 않는다.

```python
q.is_correct(2)         # 우리가 쓰는 형태 (인자 1개)
Quiz.is_correct(q, 2)   # 파이썬 내부에서 실제로 벌어지는 일 (self=q)
```

`self`라는 이름은 문법이 아니라 **관례**지만, 모든 파이썬 코드가 따르므로 반드시 지킨다.

> 📌 **이 프로젝트에서:**
> - [quiz.py:15-21](quiz.py#L15-L21) — `Quiz.__init__`이 문제 · 선택지 · 정답을 속성으로 저장한다
> - [quiz_game.py:21-24](quiz_game.py#L21-L24) — `QuizGame.__init__`은 한 걸음 더 나아가 **생성 시점에 파일을 불러온다.** `QuizGame()`을 만드는 것만으로 저장된 데이터가 복원되므로 [main.py](main.py)는 두 줄이면 된다

---

#### 속성(attribute)과 메서드(method)

| | 정의 | 품사로 보면 | 예 |
|---|---|---|---|
| **속성** | 객체가 **가지고 있는 값** | 명사 | `self.question`, `self.best_score` |
| **메서드** | 객체가 **할 수 있는 행동** | 동사 | `is_correct()`, `show()`, `save()` |

```python
class QuizGame:
    def __init__(self):
        self.quizzes = []        # 속성: 퀴즈 목록
        self.best_score = 0      # 속성: 최고 점수

    def add_quiz(self, quiz):    # 메서드: 퀴즈를 추가하는 행동
        self.quizzes.append(quiz)

    def show_score(self):        # 메서드: 점수를 보여주는 행동
        if self.best_score == 0:
            print("아직 기록이 없습니다.")
        else:
            print(f"🏆 최고 점수: {self.best_score}점")


game = QuizGame()
game.add_quiz(Quiz("문제", ["a", "b", "c", "d"], 1))
print(len(game.quizzes))    # 1   ← 속성은 () 없이 접근
game.show_score()           #     ← 메서드는 ()를 붙여 호출
```

**메서드는 다른 메서드를 부를 수 있다.** `self.`를 붙이면 같은 객체의 다른 기능을 쓸 수 있다.

```python
def play(self):
    ...
    picked = self.ask_int("정답 입력 (1-4): ", 1, 4)   # 자기 메서드 호출
    ...
    self.save()                                        # 끝나고 저장
```

**`@staticmethod` — `self`가 필요 없는 메서드**

객체가 아직 없는 상태에서 호출해야 하는 함수도 있다. "dict를 받아 Quiz 객체를 **만들어** 돌려주는" 함수는 만들기 전이므로 `self`가 존재하지 않는다.

```python
class Quiz:
    ...
    @staticmethod
    def from_dict(data):
        return Quiz(data["question"], data["choices"], data["answer"])

q = Quiz.from_dict({"question": "...", "choices": [...], "answer": 3})
# 인스턴스 없이 '클래스 이름.메서드()'로 바로 호출한다
```

> 📌 **이 프로젝트에서:**
> - 속성 → [quiz.py:19-21](quiz.py#L19-L21) (`question`/`choices`/`answer`), [quiz_game.py:23-24](quiz_game.py#L23-L24) (`quizzes`/`best_score`)
> - 메서드 → [quiz.py:23-35](quiz.py#L23-L35) (`is_correct`/`show`), [quiz_game.py:67-153](quiz_game.py#L67-L153) (`play`/`add_quiz`/`list_quizzes`/`show_score`/`save`)
> - 정적 메서드 → [quiz.py:48-55](quiz.py#L48-L55) (`from_dict`)

---

### 10.3 파일 입출력

#### 파일을 열고, 읽고, 쓰는 기본 과정

프로그램의 변수는 **메모리**에 있어서 프로그램이 끝나면 사라진다. 데이터를 다음 실행에서도 쓰려면 **디스크의 파일**에 남겨야 한다. 이것이 **데이터 영속성(persistence)** 이다.

기본 과정은 **열기 → 읽기/쓰기 → 닫기** 3단계다.

```python
# 쓰기 — "w" 모드
f = open("memo.txt", "w", encoding="utf-8")
f.write("안녕하세요\n")
f.close()          # ← 닫기를 잊으면 내용이 디스크에 안 써질 수 있다

# 읽기 — "r" 모드
f = open("memo.txt", "r", encoding="utf-8")
text = f.read()
f.close()
print(text)        # 안녕하세요
```

**하지만 실제로는 `with` 문을 쓴다.** 중간에 에러가 나도 파일이 **자동으로 닫히기** 때문이다.

```python
# 권장 방식 — 블록을 벗어나면 close()가 자동 호출된다
with open("memo.txt", "w", encoding="utf-8") as f:
    f.write("안녕하세요\n")
# 여기서 파일은 이미 닫혀 있다
```

**주요 모드**

| 모드 | 의미 | 파일이 없으면 | 기존 내용 |
|---|---|---|---|
| `"r"` | 읽기 | `FileNotFoundError` | – |
| `"w"` | 쓰기 | 새로 생성 | **전부 지워짐** |
| `"a"` | 이어쓰기 | 새로 생성 | 유지, 뒤에 추가 |

**`encoding="utf-8"`은 한글을 다룬다면 반드시 지정한다.** 생략하면 OS 기본 인코딩을 따라가서, 윈도우(cp949)와 맥/리눅스(utf-8) 사이에서 한글이 깨지는 원인이 된다.

```python
import os

if not os.path.exists("state.json"):     # 파일 존재 여부 확인
    print("저장된 데이터가 없습니다.")
```

> 📌 **이 프로젝트에서:** [storage.py:69](storage.py#L69)(읽기), [storage.py:91](storage.py#L91)(쓰기) 둘 다 `with` + `encoding="utf-8"`을 쓴다. [storage.py:63](storage.py#L63)에서 `os.path.exists`로 첫 실행 여부를 판단한다.

---

#### JSON 형식이 무엇이고, 왜 데이터 저장에 사용하는가

**JSON(JavaScript Object Notation)은 구조를 가진 데이터를 텍스트로 표현하는 표준 형식이다.** 이름에 JavaScript가 들어가지만 언어와 무관한 범용 포맷이며, 파이썬 표준 라이브러리(`json`)로 바로 다룰 수 있다.

**왜 JSON인가?** 그냥 텍스트로 저장하면 이런 문제가 생긴다.

```
HTTP 상태 코드 404가 의미하는 것은?,서버 내부 오류,요청 성공,찾을 수 없음,권한 없음,3
```

- 문제 안에 쉼표가 들어가면 즉시 깨진다
- 중첩 구조(리스트 안의 리스트)를 표현할 수 없다
- 숫자 `3`인지 문자열 `"3"`인지 구분되지 않는다
- 다시 읽을 때 쪼개는 규칙을 직접 만들어야 한다

JSON은 이 문제를 전부 해결한다.

1. **구조를 그대로 표현** — 중첩된 객체/배열을 있는 그대로 저장한다
2. **타입이 보존된다** — 숫자 / 문자열 / 불리언 / null이 구분된다
3. **파싱 코드가 필요 없다** — `json.load()` 한 줄이면 파이썬 dict/list로 복원된다
4. **사람이 읽을 수 있다** — 텍스트라서 에디터로 열어 확인 · 수정할 수 있다
5. **표준이다** — 웹 API · 설정 파일 등 어디서나 통용된다

**파이썬 ↔ JSON 타입 대응**

| Python | JSON |
|---|---|
| `dict` | object `{ }` |
| `list` | array `[ ]` |
| `str` | string |
| `int`, `float` | number |
| `True` / `False` | `true` / `false` |
| `None` | `null` |

**핵심 함수 4가지** — 이름에 `s`가 붙으면 **s**tring(문자열) 대상이다.

```python
import json

data = {"quizzes": [{"question": "...", "answer": 3}], "best_score": 83}

# 파이썬 객체 → JSON 파일
with open("state.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

# JSON 파일 → 파이썬 객체
with open("state.json", "r", encoding="utf-8") as f:
    loaded = json.load(f)
print(loaded["best_score"])     # 83

# 문자열 버전 (파일 없이 메모리에서)
text = json.dumps(data, ensure_ascii=False)    # 객체 → 문자열
back = json.loads(text)                        # 문자열 → 객체
```

**중요한 두 옵션**

| 옵션 | 빼면 | 넣으면 |
|---|---|---|
| `ensure_ascii=False` | 한글이 `"\ud55c\uae00"` 형태로 이스케이프됨 | 한글이 그대로 저장됨 |
| `indent=2` | 전부 한 줄로 붙어 나옴 | 들여쓰기가 들어가 읽기 좋음 |

**JSON이 저장하지 못하는 것** — `json` 모듈은 `dict`/`list`/`str`/`int`/`float`/`bool`/`None`만 안다. **`Quiz` 같은 사용자 정의 객체는 저장할 수 없다.** 그래서 변환하는 다리가 필요하다.

```python
raw = [q.to_dict() for q in self.quizzes]                # 저장: 객체 → dict
self.quizzes = [Quiz.from_dict(q) for q in raw_quizzes]  # 복원: dict → 객체
```

> 📌 **이 프로젝트에서:** [`save_state`](storage.py#L84) · [`load_state`](storage.py#L54)가 파일을 다루고, 변환 다리는 [quiz.py:37-55](quiz.py#L37-L55)와 [quiz_game.py:24](quiz_game.py#L24) · [:152](quiz_game.py#L152)에 있다. 저장 형식은 [7장](#7-데이터-파일-statejson) 참고.

---

#### try / except로 오류 처리하기

**예외(exception)는 실행 중에 발생하는 오류다.** 처리하지 않으면 프로그램이 트레이스백을 뱉으며 즉시 죽는다. `try/except`는 "오류가 날 수 있는 코드를 감싸고, 나면 이렇게 대응하라"고 지정하는 문법이다.

```python
try:
    number = int(input("숫자: "))     # 오류가 날 수 있는 코드
except ValueError:
    print("⚠️ 숫자가 아닙니다.")       # ValueError가 났을 때
else:
    print(f"입력값: {number}")        # 오류가 안 났을 때만 (선택)
finally:
    print("입력 처리 완료")           # 오류 여부와 무관하게 항상 (선택)
```

**자주 만나는 예외**

| 예외 | 언제 발생하는가 |
|---|---|
| `FileNotFoundError` | 없는 파일을 `"r"`로 열 때 |
| `json.JSONDecodeError` | 파일 내용이 올바른 JSON이 아닐 때 |
| `KeyError` | dict에 없는 키를 꺼낼 때 |
| `ValueError` | `int("abc")`처럼 변환이 불가능할 때 |
| `IndexError` | 리스트 범위 밖 인덱스 접근 |
| `ZeroDivisionError` | 0으로 나눌 때 |
| `OSError` | 권한 없음, 디스크 문제 등 |
| `KeyboardInterrupt` | 사용자가 `Ctrl+C`를 눌렀을 때 |
| `EOFError` | 입력 스트림이 끝났을 때 |

**여러 예외를 한 번에 잡기** — 대응 방법이 같다면 튜플로 묶는다.

```python
try:
    with open("state.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    return data["quizzes"], data["best_score"]
except (json.JSONDecodeError, KeyError, OSError) as e:
    # JSONDecodeError: 내용 깨짐 / KeyError: 키 누락 / OSError: 읽기 실패
    print(f"⚠️ 데이터 파일이 손상되어 기본 퀴즈로 복구합니다. ({e})")
    return list(DEFAULT_QUIZZES), 0     # 죽지 않고 '기본값으로 복구'
```

`as e`로 예외 객체를 받아 원인을 함께 출력하면 디버깅이 쉬워진다.

**⚠️ 하지 말아야 할 것 — 맨손 `except`**

```python
try:
    ...
except:                 # ❌ 모든 예외를 다 삼킨다. Ctrl+C까지 잡아버리고,
    pass                #    무엇이 잘못됐는지 영영 알 수 없다
```

**잡을 예외를 구체적으로 지정**하는 것이 원칙이다. 예상한 오류만 처리하고, 예상 못 한 오류는 드러나게 두어야 버그를 발견할 수 있다.

**"미리 확인" vs "일단 해보고 처리"**

```python
# 방법 1 — 확인 후 실행 (LBYL: Look Before You Leap)
if os.path.exists(STATE_FILE):
    ...

# 방법 2 — 일단 시도하고 예외 처리 (EAFP: Easier to Ask Forgiveness than Permission)
try:
    with open(STATE_FILE) as f: ...
except FileNotFoundError:
    ...
```

파이썬은 보통 방법 2를 선호하지만, 이 프로젝트는 "파일이 없는 것(정상적인 첫 실행)"과 "파일이 깨진 것(비정상)"을 **다른 메시지로 안내**하기 위해 두 방법을 함께 썼다.

> 📌 **이 프로젝트에서:**
> - [storage.py:68-81](storage.py#L68-L81) — 손상된 JSON을 잡아 기본 데이터로 복구
> - [storage.py:90-96](storage.py#L90-L96) — 저장 실패(`OSError`)를 잡아 안내만 하고 게임은 계속 진행
> - [quiz_game.py:161-180](quiz_game.py#L161-L180) — `Ctrl+C`와 입력 종료를 잡아 **저장한 뒤** 종료. 예외 처리를 "죽지 않게 하는 것"을 넘어 **"데이터를 잃지 않게 하는 것"** 에 쓴 사례다

---

### 10.4 Git 기초

#### Git이 무엇이고 왜 필요한가

**Git은 분산 버전 관리 시스템(DVCS)이다.** 파일의 변경 이력을 **스냅샷 단위(커밋)** 로 기록하고, 원하는 시점으로 되돌리거나 여러 갈래의 작업을 나눠 진행하다 합칠 수 있게 해준다.

Git 없이 개발하면 이런 일이 벌어진다.

```
최종.py
최종_수정.py
최종_진짜최종.py
최종_진짜최종_v2_이걸로제출.py     ← 무엇이 뭔지 알 수 없다
```

**Git이 해결하는 것**

1. **이력 관리** — 언제, 누가, 무엇을, 왜 바꿨는지 커밋 메시지와 함께 남는다
2. **되돌리기** — 잘못 고쳐도 이전 커밋으로 안전하게 복구할 수 있다
3. **병렬 작업** — 새 기능을 시도하는 동안 동작하는 버전(main)은 그대로 둔다
4. **협업** — 여러 명이 같은 프로젝트를 각자 수정하고 합칠 수 있다
5. **백업** — 원격 저장소에 push하면 로컬 PC가 고장나도 코드가 남는다

> **Git ≠ GitHub** — Git은 내 컴퓨터에서 돌아가는 **프로그램**이고, GitHub는 Git 저장소를 올려두는 **웹 서비스**다. Git만으로도 버전 관리는 완전히 가능하다.

**3개의 영역 + 원격** — Git 명령을 이해하는 핵심 모델이다.

```
   작업 디렉토리        스테이징 영역        로컬 저장소         원격 저장소
   (Working Dir)  ──▶  (Staging Area) ──▶  (Local Repo)  ◀──▶  (GitHub)
      파일 수정           git add            git commit      git push / pull
```

"수정했다"와 "기록으로 남기겠다"를 분리한 것이 Git의 특징이다. 그래서 **여러 파일을 고쳤어도 관련 있는 것만 골라 `add`해서 의미 있는 단위로 커밋**할 수 있다.

---

#### 핵심 명령어 7개

**`git init` — 저장소 만들기**

현재 폴더를 Git 저장소로 만든다. `.git` 폴더가 생기며 여기에 모든 이력이 저장된다. 프로젝트당 딱 한 번만 실행한다.

```bash
git init
git status          # 현재 상태 확인 — 가장 자주 쓰는 명령
```

**`git add` — 커밋할 변경 사항 선택 (스테이징)**

"이번 커밋에 이 파일의 변경을 포함하겠다"고 표시한다. **커밋의 범위를 직접 고르는 단계**다.

```bash
git add quiz.py             # 특정 파일만
git add quiz.py storage.py  # 여러 파일
git add .                   # 현재 폴더의 모든 변경 (가장 흔하게 씀)
```

**`git commit` — 기록으로 확정**

스테이징된 변경을 하나의 스냅샷으로 저장소에 기록한다. 이 시점으로 언제든 돌아올 수 있다.

```bash
git commit -m "Feat: 퀴즈 목록 기능 구현"
git log --oneline           # 커밋 이력 한 줄씩 보기
```

커밋 메시지는 **무엇을 왜 했는지** 알 수 있게 쓴다. 이 프로젝트는 `Feat:`(기능) · `Fix:`(수정) · `Docs:`(문서) 접두어 관례를 따랐다.

```
4968dcf docs: readme troubleshooting add
e512717 Merge pull request #1 from JunHyeok-Cha/feature/play
69baf6a Feat: state.json 저장/불러오기 구현
6e2bbca Feat: 점수 확인 및 최고점수 갱신
cb57a12 Feat: 퀴즈 목록 기능 구현
```

**`git push` — 로컬 커밋을 원격으로 올리기**

커밋은 아직 **내 컴퓨터에만** 있다. GitHub에 반영하려면 push해야 한다.

```bash
git remote add origin https://github.com/사용자명/저장소명.git   # 원격 등록 (최초 1회)
git push -u origin main     # -u: 추적 연결 설정 (최초 1회)
git push                    # 이후로는 이것만
```

**`git pull` — 원격의 변경을 내 로컬로 가져오기**

다른 사람이(또는 다른 PC에서) 올린 커밋을 받아온다. 내부적으로 `fetch`(가져오기) + `merge`(합치기)다.

```bash
git pull                    # 작업 시작 전에 습관적으로 실행하면 충돌이 줄어든다
```

**`git checkout` — 브랜치/시점 이동**

```bash
git checkout feature/play       # 기존 브랜치로 이동
git checkout -b feature/play    # 브랜치를 만들면서 동시에 이동 (-b = branch)
git checkout main               # main으로 복귀
```

> 최신 Git에서는 역할을 나눈 `git switch`(브랜치 이동)와 `git restore`(파일 복원)를 권장하지만, `checkout`도 그대로 동작한다.

**`git clone` — 원격 저장소를 통째로 복제**

`init`과 달리 **이미 존재하는** 저장소를 전체 커밋 이력까지 포함해 내려받는다. 원격 주소(`origin`)도 자동 등록된다.

```bash
git clone https://github.com/JunHyeok-Cha/Codyssey-week2-quizgame.git
```

**한눈에 보기**

| 명령 | 하는 일 | 언제 |
|---|---|---|
| `git init` | 새 저장소 생성 | 프로젝트 시작 시 1회 |
| `git clone` | 기존 원격 저장소 복제 | 저장소를 처음 받아올 때 |
| `git add` | 커밋에 포함할 변경 선택 | 커밋 직전 |
| `git commit` | 스냅샷으로 확정 | 의미 있는 작업 단위마다 |
| `git push` | 로컬 커밋 → 원격 | 커밋 후 공유 · 백업 |
| `git pull` | 원격 커밋 → 로컬 | 작업 시작 전 |
| `git checkout` | 브랜치 / 시점 이동 | 작업 갈래를 바꿀 때 |
| `git status` | 현재 상태 확인 | 수시로 |
| `git log` | 커밋 이력 확인 | 수시로 |

**`.gitignore`** — 버전 관리에서 제외할 파일을 지정한다. 자동 생성물이나 로컬 데이터는 커밋하지 않는다.

```gitignore
# 파이썬 캐시
__pycache__/
*.pyc

# 로컬 데이터 (코드에 기본 퀴즈가 내장돼 있어 없어도 실행됨)
state.json

# OS / 에디터
.DS_Store
.vscode/
.idea/
```

---

#### 브랜치 생성과 병합

**브랜치는 커밋 이력의 갈래다.** main을 건드리지 않고 별도 갈래에서 기능을 만들다가, 완성되면 main에 합친다. 덕분에 main은 항상 **동작하는 상태**로 유지된다.

```
main          A───B───────────────E (merge)
                   \             /
feature/play        C───────D───┘
```

**전체 흐름**

```bash
# 1) 브랜치 생성 + 이동
git checkout -b feature/play

# 2) 작업하고 커밋
git add quiz_game.py
git commit -m "Feat: 퀴즈 풀기 기능 구현"

# 3) 원격에도 브랜치를 만들고 추적 연결 (-u는 최초 1회)
git push -u origin feature/play

# 4) main으로 돌아와 최신 상태로 갱신
git checkout main
git pull

# 5) 병합 — --no-ff로 머지 커밋을 남긴다
git merge --no-ff feature/play -m "Merge: 퀴즈 풀기 기능 병합"
git push

# 6) 병합이 끝난 브랜치 정리 (선택)
git branch -d feature/play                # 로컬 삭제
git push origin --delete feature/play     # 원격 삭제
```

**`--no-ff`를 쓰는 이유**

main에 새 커밋이 없으면 Git은 브랜치 포인터만 앞으로 옮기는 **fast-forward** 병합을 한다. 결과 코드는 같지만 **"갈라졌다 합쳐졌다"는 흔적이 이력에 남지 않는다.** `--no-ff`는 머지 커밋을 강제로 만들어 그 기록을 보존한다. → [9장 트러블슈팅 4](#4-로컬-브랜치가-github에-안-보이고-병합-기록도-안-남음)에서 실제로 겪은 문제다.

**브랜치 확인**

```bash
git branch                          # 로컬 브랜치 목록 (*가 현재 위치)
git branch -r                       # 원격 브랜치 목록
git branch -a                       # 전부
git log --oneline --graph --all     # 갈라지고 합쳐진 모양을 그림으로 확인
```

**충돌(conflict)** — 두 브랜치가 **같은 파일의 같은 줄**을 다르게 고쳤을 때 Git이 자동 병합을 포기하고 사람에게 넘긴다.

```python
<<<<<<< HEAD
print("현재 브랜치(main)의 내용")
=======
print("병합하려는 브랜치의 내용")
>>>>>>> feature/play
```

`<<<<<<<`, `=======`, `>>>>>>>` 표시를 **직접 지우고** 최종 코드만 남긴 뒤 커밋하면 해결된다.

```bash
git add 충돌파일.py
git commit          # 머지 커밋 완료
```

**Pull Request(PR)로 병합하기** — 실무에서 더 일반적인 방식이다. 브랜치를 push한 뒤 GitHub에서 PR을 만들면 병합 전에 코드 리뷰를 거칠 수 있고, 논의 내용이 Pull requests 탭에 영구 보존된다.

> 📌 **이 프로젝트에서:** `feature/play` 브랜치에서 퀴즈 풀기 기능을 구현한 뒤 **PR #1로 main에 병합**했다 (커밋 `e512717`).

---

#### 원격 저장소 clone하고 pull로 가져오기

**시나리오 1 — 다른 PC에서 이 프로젝트를 이어서 작업하기**

```bash
git clone https://github.com/JunHyeok-Cha/Codyssey-week2-quizgame.git
cd Codyssey-week2-quizgame
python3 main.py         # 바로 실행 가능 (외부 라이브러리 없음)
```

`clone`은 최신 코드뿐 아니라 **전체 커밋 이력과 브랜치 정보**까지 받아온다. `origin`도 자동 등록되므로 `git remote add`를 따로 할 필요가 없다.

**시나리오 2 — 협업 중 남의 변경사항 받아오기**

```bash
git pull                # = git fetch + git merge
```

**`fetch`와 `pull`의 차이**

```bash
git fetch origin                        # 가져오기만 함 — 내 작업은 그대로
git log HEAD..origin/main --oneline     # 무엇이 새로 왔는지 먼저 확인
git merge origin/main                   # 확인 후 직접 합치기

git pull                                # 위 두 단계를 한 번에
```

내 작업이 진행 중일 때는 `fetch`로 먼저 확인하는 편이 안전하다.

**협업 시 권장 흐름**

```bash
git pull                           # 1. 최신 상태로 맞추기
git checkout -b feature/새기능      # 2. 브랜치 생성
# ... 작업 ...
git add .                          # 3. 스테이징
git commit -m "Feat: ..."          # 4. 커밋
git push -u origin feature/새기능   # 5. 원격에 올리기
                                   # 6. GitHub에서 PR 생성 → 리뷰 → 병합
git checkout main && git pull      # 7. 병합 결과를 로컬에 반영
```

> **참고:** `checkout` · `pull` · `clone`은 "가져오거나 이동하는" 동작이라 커밋을 만들지 않으므로 GitHub 이력에 남지 않는다. 수행 증거가 필요하면 터미널 화면을 스크린샷으로 남긴다.
