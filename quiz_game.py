"""
quiz_game.py
게임 전체를 관리하는 QuizGame 클래스.

[역할]
- 메뉴 표시 / 사용자 입력 받기
- 퀴즈 풀기 / 추가 / 목록 / 점수 확인
- storage 모듈을 통해 저장·불러오기

[설계 원칙]
'입력을 안전하게 받는 일'(ask_int)을 한 곳에 모아 재사용한다.
메뉴 선택, 정답 입력, 정답 번호 입력이 모두 같은 방어 로직을 필요로 하기 때문이다.
= 중복 제거(DRY: Don't Repeat Yourself).
"""

from quiz import Quiz
import storage


class QuizGame:
    def __init__(self):
        # storage에서 dict 리스트로 불러온 뒤, Quiz 객체 리스트로 변환한다.
        raw_quizzes, self.best_score = storage.load_state()
        self.quizzes = [Quiz.from_dict(q) for q in raw_quizzes]

    # ─────────────────────────────────────────────────────────
    # 공통 입력 헬퍼: 숫자 입력을 안전하게 받는다.
    # 과제의 '공통 입력/예외 처리 기준'을 이 함수 하나로 충족한다.
    # ─────────────────────────────────────────────────────────
    def ask_int(self, prompt, low, high):
        """
        low~high 범위의 정수를 받을 때까지 반복해서 물어본다.
        - 앞뒤 공백 제거
        - 빈 입력 / 숫자 아님 / 범위 밖 → 안내 후 재입력
        """
        while True:
            raw = input(prompt).strip()   # strip(): 앞뒤 공백 제거
            if raw == "":
                print("⚠️ 빈 입력입니다. 다시 입력하세요.")
                continue
            if not raw.lstrip("-").isdigit():   # 숫자로 변환 가능한지 확인
                print("⚠️ 숫자만 입력할 수 있습니다.")
                continue
            value = int(raw)
            if value < low or value > high:
                print(f"⚠️ {low}~{high} 사이의 숫자를 입력하세요.")
                continue
            return value

    # ─────────────────────────────────────────────────────────
    # 메뉴 출력
    # ─────────────────────────────────────────────────────────
    def show_menu(self):
        print("\n" + "=" * 40)
        print("        🎯 나만의 퀴즈 게임 🎯")
        print("=" * 40)
        print("1. 퀴즈 풀기")
        print("2. 퀴즈 추가")
        print("3. 퀴즈 목록")
        print("4. 점수 확인")
        print("5. 종료")
        print("=" * 40)

    # ─────────────────────────────────────────────────────────
    # 1. 퀴즈 풀기
    # ─────────────────────────────────────────────────────────
    def play(self):
        if not self.quizzes:      # 리스트가 비어있으면 (퀴즈가 하나도 없으면)
            print("\n등록된 퀴즈가 없습니다. 먼저 퀴즈를 추가하세요.")
            return

        total = len(self.quizzes)
        print(f"\n📝 퀴즈를 시작합니다! (총 {total}문제)")
        score = 0

        for i, quiz in enumerate(self.quizzes, start=1):
            print("\n" + "-" * 40)
            quiz.show(index=i)
            picked = self.ask_int("정답 입력 (1-4): ", 1, 4)
            if quiz.is_correct(picked):
                print("✅ 정답입니다!")
                score += 1
            else:
                print(f"❌ 오답입니다. 정답은 {quiz.answer}번.")

        # 점수 = 맞힌 문제 수를 100점 만점으로 환산
        points = round(score / total * 100)
        print("\n" + "=" * 40)
        print(f"🏆 결과: {total}문제 중 {score}문제 정답! ({points}점)")

        # 최고점수 갱신 판단
        if points > self.best_score:
            self.best_score = points
            print("🎉 새로운 최고 점수입니다!")
        print("=" * 40)

        self.save()   # 점수가 바뀌었을 수 있으니 저장
   
    # ─────────────────────────────────────────────────────────
    # 2. 퀴즈 추가
    # ─────────────────────────────────────────────────────────
    def add_quiz(self):
        print("\n📌 새로운 퀴즈를 추가합니다.")
        question = input("문제를 입력하세요: ").strip()
        if question == "":
            print("⚠️ 문제가 비어 있어 추가를 취소합니다.")
            return

        choices = []
        for n in range(1, 5):    # 선택지 4개를 순서대로 입력받음
            while True:
                c = input(f"선택지 {n}: ").strip()
                if c == "":
                    print("⚠️ 선택지는 비울 수 없습니다.")
                    continue
                choices.append(c)
                break

        answer = self.ask_int("정답 번호 (1-4): ", 1, 4)

        # 새 Quiz 객체를 만들어 목록에 추가
        self.quizzes.append(Quiz(question, choices, answer))
        self.save()
        print("✅ 퀴즈가 추가되었습니다!")
        
    # ─────────────────────────────────────────────────────────
    # 3. 퀴즈 목록
    # ─────────────────────────────────────────────────────────


    # ─────────────────────────────────────────────────────────
    # 4. 점수 확인
    # ─────────────────────────────────────────────────────────


    # ─────────────────────────────────────────────────────────
    # 저장: Quiz 객체 → dict 로 바꿔 storage에 넘긴다
    # ─────────────────────────────────────────────────────────


    # ─────────────────────────────────────────────────────────
    # 메인 루프
    # ─────────────────────────────────────────────────────────
    def run(self):
        # KeyboardInterrupt(Ctrl+C), EOFError(입력 종료)에도 안전하게 종료
        try:
            while True:
                self.show_menu()
                choice = self.ask_int("선택: ", 1, 5)
                if choice == 1:
                    self.play()
                elif choice == 2:
                    self.add_quiz()
                elif choice == 3:
                    self.list_quizzes()
                elif choice == 4:
                    self.show_score()
                elif choice == 5:
                    print("\n👋 게임을 종료합니다. 안녕히 가세요!")
                    self.save()
                    break
        except (KeyboardInterrupt, EOFError):
            # 비정상 종료 대신, 저장 후 깔끔하게 마무리
            print("\n\n⚠️ 입력이 중단되었습니다. 저장 후 종료합니다.")
            self.save()
