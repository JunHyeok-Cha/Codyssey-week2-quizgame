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


