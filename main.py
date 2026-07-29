"""
main.py
프로그램의 진입점(entry point).

[왜 이렇게 얇은가?]
main은 '시작 버튼' 역할만 한다. 실제 로직은 QuizGame이 갖는다.
이렇게 하면 나중에 다른 방식으로 게임을 실행하고 싶을 때(예: 테스트) QuizGame만
가져다 쓰면 된다.

[if __name__ == "__main__" 은 무엇인가?]
이 파일을 'python main.py'로 직접 실행할 때만 아래 블록이 돌아간다.
다른 파일에서 import 할 때는 실행되지 않는다. 파이썬의 표준 관용구다.
"""

from quiz_game import QuizGame


def main():
    game = QuizGame()   # 데이터 불러오기(생성자에서 처리)
    game.run()          # 메뉴 루프 시작


if __name__ == "__main__":
    main()
