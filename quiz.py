"""
quiz.py
개별 퀴즈 1개를 표현하는 Quiz 클래스.

[왜 클래스로 만드는가?]
퀴즈 하나는 '문제 + 선택지 4개 + 정답번호'가 항상 함께 다니는 한 덩어리다.
이걸 dict로만 다루면 quiz["question"], quiz["answer"] 처럼 키를 매번 외워야 하고
오타(quiz["anser"])가 나도 실행 전까지 모른다.
클래스로 묶으면 q.question, q.is_correct(3) 처럼 '이 데이터로 할 수 있는 행동'까지
한 곳에 모이므로, 문제와 관련된 로직이 흩어지지 않는다.

[파이썬은 왜 멤버를 미리 선언하지 않는가]
- 파이썬은 Java/C++과 달리 클래스 상단에 멤버를 선언하지 않고, `self.question = question`처럼 값을 대입하는 순간 속성이 생성된다.
- 객체가 속성을 내부 딕셔너리(`__dict__`)로 관리하기 때문이다.
- 그래서 "객체의 모든 속성은 `__init__`에서 초기화한다"는 관례를 지킨다. `__init__`만 보면 이 객체가 어떤 속성을 갖는지 한눈에 파악되기 때문이다.
"""


class Quiz:
    def __init__(self, question, choices, answer):
        # __init__ 은 인스턴스가 만들어질 때 자동 호출되는 '생성자'.
        # self 는 '지금 만들어지는 이 퀴즈 자신'을 가리킨다.
        # 아래 3줄은 넘겨받은 값을 이 인스턴스의 속성(attribute)으로 저장한다.
        self.question = question          # 문제 문자열
        self.choices = choices            # 선택지 리스트 (원소 4개)
        self.answer = answer              # 정답 번호 (1~4 중 하나, int)

    def is_correct(self, user_choice):
        """사용자가 고른 번호가 정답인지 True/False로 반환."""
        return user_choice == self.answer

    def show(self, index=None):
        """문제와 선택지를 화면에 출력한다. index는 '[문제 3]'처럼 순번 표시용."""
        header = f"[문제 {index}]" if index is not None else "[문제]"
        print(header)
        print(self.question)
        print()
        # enumerate(..., start=1) → (1, 첫선택지), (2, 두번째)... 로 번호를 붙여준다.
        for number, choice in enumerate(self.choices, start=1):
            print(f"  {number}. {choice}")

    def to_dict(self):
        """
        JSON으로 저장하려면 객체를 순수 dict로 바꿔야 한다.
        (json 모듈은 Quiz 객체를 어떻게 저장할지 모르기 때문)
        """
        return {
            "question": self.question,
            "choices": self.choices,
            "answer": self.answer,
        }

    @staticmethod
    def from_dict(data):
        """
        반대로, 파일에서 읽은 dict를 다시 Quiz 객체로 되살린다.
        @staticmethod: self가 필요없는(특정 인스턴스에 속하지 않는) 함수라는 표시.
        Quiz.from_dict(d) 형태로 인스턴스 없이 바로 호출한다.
        """
        return Quiz(data["question"], data["choices"], data["answer"])
