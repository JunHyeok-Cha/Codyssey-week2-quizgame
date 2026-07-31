"""
storage.py
파일 입출력(JSON 저장/불러오기)만 담당하는 모듈.

[왜 저장 로직을 따로 빼는가?]
QuizGame은 '게임 흐름'에 집중해야 한다. "어떤 파일에 어떤 형식으로 저장하느냐"는
별개의 관심사다. 이걸 분리해두면 나중에 저장 방식을 바꿔도(JSON→DB 등)
QuizGame 코드는 손대지 않는다. = 관심사의 분리(Separation of Concerns).
"""

import json
import os

# 데이터 파일 경로. 과제 규칙: '프로젝트 루트의 state.json'.
STATE_FILE = "state.json"


# 파일이 아예 없을 때(첫 실행) 사용할 기본 퀴즈 데이터.
# 주제: '기초 컴퓨터/개발 상식' — 5개 이상 요구 충족.
DEFAULT_QUIZZES = [
    {
        "question": "HTTP 상태 코드 404가 의미하는 것은?",
        "choices": ["서버 내부 오류", "요청 성공", "찾을 수 없음", "권한 없음"],
        "answer": 3,
    },
    {
        "question": "다음 중 파이썬에서 '변경 불가능(immutable)'한 자료형은?",
        "choices": ["list", "dict", "set", "tuple"],
        "answer": 4,
    },
    {
        "question": "Git에서 변경 이력을 기록으로 확정하는 명령은?",
        "choices": ["git add", "git commit", "git status", "git clone"],
        "answer": 2,
    },
    {
        "question": "1 바이트(byte)는 몇 비트(bit)인가?",
        "choices": ["4", "8", "16", "32"],
        "answer": 2,
    },
    {
        "question": "JSON에서 데이터를 담는 두 가지 기본 구조는?",
        "choices": ["객체와 배열", "함수와 변수", "클래스와 객체", "행과 열"],
        "answer": 1,
    },
    {
        "question": "터미널에서 현재 위치(디렉토리)를 출력하는 명령은?",
        "choices": ["ls", "cd", "pwd", "mkdir"],
        "answer": 3,
    },
]


def load_state():
    """
    state.json을 읽어 (quizzes 리스트, best_score) 를 돌려준다.
    3가지 경우를 모두 안전하게 처리한다:
      1) 파일이 없다      → 기본 데이터로 시작
      2) 파일이 깨졌다    → 안내 후 기본 데이터로 복구
      3) 정상             → 파일 내용 사용
    """
    # 경우 1: 파일 자체가 없음 (첫 실행)
    if not os.path.exists(STATE_FILE):
        print("📂 저장된 데이터가 없어 기본 퀴즈로 시작합니다.")
        return list(DEFAULT_QUIZZES), 0

    # 경우 2/3: 파일은 있으나 내용이 깨졌을 수 있음 → try/except로 방어
    try:
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)          # JSON 문자열 → 파이썬 dict
        quizzes = data["quizzes"]
        best_score = data["best_score"]
        print(f"📂 저장된 데이터를 불러왔습니다. "
              f"(퀴즈 {len(quizzes)}개, 최고점수 {best_score}점)")
        return quizzes, best_score
    except (json.JSONDecodeError, KeyError, OSError) as e:
        # JSONDecodeError: 파일 내용이 올바른 JSON이 아님
        # KeyError: quizzes/best_score 키가 없음(형식 손상)
        # OSError: 읽기 권한 문제 등
        print(f"⚠️ 데이터 파일이 손상되어 기본 퀴즈로 복구합니다. ({e})")
        return list(DEFAULT_QUIZZES), 0


def save_state(quizzes, best_score):
    """
    현재 퀴즈 목록과 최고점수를 state.json에 저장한다.
    quizzes는 dict들의 리스트라고 가정한다(호출부에서 to_dict 처리).
    """
    data = {"quizzes": quizzes, "best_score": best_score}
    try:
        with open(STATE_FILE, "w", encoding="utf-8") as f:
            # ensure_ascii=False → 한글이 \uXXXX로 깨지지 않고 그대로 저장됨
            # indent=2 → 사람이 읽기 좋게 들여쓰기
            json.dump(data, f, ensure_ascii=False, indent=2)
    except OSError as e:
        print(f"⚠️ 저장에 실패했습니다. ({e})")


