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
DEFAULT_QUIZZES = [
    {
      "question": "마지막으로 인피니티 스톤을 이용해 핑거스냅을 한 인물은?",
      "choices": [
        "타노스",
        "헐크",
        "아이언맨",
        "토르"
      ],
      "answer": 3,
      "hint": "지구 출신"
    },
    {
      "question": "인피니티 스톤의 갯수는?",
      "choices": [
        "3개",
        "4개",
        "5개",
        "6개"
      ],
      "answer": 4,
    },
    {
      "question": "가디언즈 오브 갤럭시에서 가장 많이 나오는 대사는?",
      "choices": [
        "가모라",
        "I am Groot",
        "Hey, Peter",
        "I am Iron Man"
      ],
      "answer": 2,
      "hint": "나무"
    },
    {
      "question": "토르의 망치를 들 수 없는 사람은?",
      "choices": [
        "캡틴 아메리카",
        "오딘",
        "헐크",
        "비전"
      ],
      "answer": 3,
      "hint": "가장 큼"
    },
    {
      "question": "스파이더맨에 나오는 악당이 아닌 인물은?",
      "choices": [
        "완다",
        "일렉트로",
        "베놈",
        "그린 고블린"
      ],
      "answer": 1,
      "hint": "마법"
    }
]



def load_state():
    """
    state.json을 읽어 (quizzes 리스트, best_score, history 리스트) 를 돌려준다.
    3가지 경우를 모두 안전하게 처리한다:
      1) 파일이 없다      → 기본 데이터로 시작
      2) 파일이 깨졌다    → 안내 후 기본 데이터로 복구
      3) 정상             → 파일 내용 사용
    """
    # 경우 1: 파일 자체가 없음 (첫 실행)
    if not os.path.exists(STATE_FILE):
        print("📂 저장된 데이터가 없어 기본 퀴즈로 시작합니다.")
        return list(DEFAULT_QUIZZES), 0, []

    # 경우 2/3: 파일은 있으나 내용이 깨졌을 수 있음 → try/except로 방어
    try:
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)          # JSON 문자열 → 파이썬 dict
        quizzes = data["quizzes"]
        best_score = data["best_score"]
        # history는 data.get()으로 꺼낸다.
        # 기록 기능이 생기기 전에 저장된 파일에는 "history" 키가 아예 없는데,
        # data["history"]로 꺼내면 KeyError → '손상된 파일'로 오해받아
        # 멀쩡한 퀴즈까지 기본값으로 덮어써진다. get()이면 빈 기록으로 시작한다.
        history = data.get("history", [])
        print(f"📂 저장된 데이터를 불러왔습니다. "
              f"(퀴즈 {len(quizzes)}개, 최고점수 {best_score}점, "
              f"기록 {len(history)}건)")
        return quizzes, best_score, history
    except (json.JSONDecodeError, KeyError, OSError) as e:
        # JSONDecodeError: 파일 내용이 올바른 JSON이 아님
        # KeyError: quizzes/best_score 키가 없음(형식 손상)
        # OSError: 읽기 권한 문제 등
        print(f"⚠️ 데이터 파일이 손상되어 기본 퀴즈로 복구합니다. ({e})")
        return list(DEFAULT_QUIZZES), 0, []


def save_state(quizzes, best_score, history):
    """
    현재 퀴즈 목록 · 최고점수 · 게임 기록을 state.json에 저장한다.
    quizzes와 history는 dict들의 리스트라고 가정한다(호출부에서 to_dict 처리).
    """
    data = {"quizzes": quizzes, "best_score": best_score, "history": history}
    try:
        with open(STATE_FILE, "w", encoding="utf-8") as f:
            # ensure_ascii=False → 한글이 \uXXXX로 깨지지 않고 그대로 저장됨
            # indent=2 → 사람이 읽기 좋게 들여쓰기
            json.dump(data, f, ensure_ascii=False, indent=2)
    except OSError as e:
        print(f"⚠️ 저장에 실패했습니다. ({e})")


