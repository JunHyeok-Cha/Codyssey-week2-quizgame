"""
quiz_game.py
게임 전체를 관리하는 QuizGame 클래스.

[역할]
- 메뉴 표시 / 사용자 입력 받기
- 퀴즈 풀기 / 추가 / 목록 / 삭제 / 점수 확인 / 기록 보기
- storage 모듈을 통해 저장·불러오기

[설계 원칙]
'입력을 안전하게 받는 일'(ask_int)을 한 곳에 모아 재사용한다.
메뉴 선택, 문제 수 선택, 정답 입력, 정답 번호 입력, 삭제할 번호 입력이
모두 같은 방어 로직을 필요로 하기 때문이다.
= 중복 제거(DRY: Don't Repeat Yourself).
"""

import random                    # 문제 순서를 섞기 위해 사용
from datetime import datetime    # 게임 기록에 날짜/시간을 남기기 위해 사용

from quiz import Quiz
import storage

# 힌트를 요청할 때 정답 대신 입력하는 글자.
# 상수로 빼두면 'h' 를 다른 글자로 바꿀 때 한 곳만 고치면 된다.
HINT_KEY = "h"

# 힌트를 쓴 문제는 맞혀도 0.5문제만 인정한다(= 점수 절반 차감).
HINT_WEIGHT = 0.5


class QuizGame:
    def __init__(self):
        # storage에서 dict 리스트로 불러온 뒤, Quiz 객체 리스트로 변환한다.
        raw_quizzes, self.best_score, self.history = storage.load_state()
        self.quizzes = [Quiz.from_dict(q) for q in raw_quizzes]

    # ─────────────────────────────────────────────────────────
    # 공통 입력 헬퍼: 숫자 입력을 안전하게 받는다.
    # 과제의 '공통 입력/예외 처리 기준'을 이 함수 하나로 충족한다.
    # ─────────────────────────────────────────────────────────
    def ask_int(self, prompt, low, high, hint_key=None):
        """
        low~high 범위의 정수를 받을 때까지 반복해서 물어본다.
        - 앞뒤 공백 제거
        - 빈 입력 / 숫자 아님 / 범위 밖 → 안내 후 재입력

        hint_key를 넘기면(예: "h") 그 글자를 입력했을 때 숫자 대신
        그 글자를 그대로 돌려준다. 호출부는 반환값이 int인지 확인해
        '정답을 골랐는지' / '힌트를 요청했는지'를 구분한다.
        """
        while True:
            raw = input(prompt).strip()   # strip(): 앞뒤 공백 제거
            if raw == "":
                print("⚠️ 빈 입력입니다. 다시 입력하세요.")
                continue
            # 힌트 요청은 숫자 변환보다 먼저 확인한다. lower()로 'H'도 허용.
            if hint_key is not None and raw.lower() == hint_key:
                return hint_key
            try:
                value = int(raw)          # 변환 시도
            except ValueError:            # 숫자가 아니면 여기로
                print("⚠️ 숫자만 입력할 수 있습니다.")
                continue
            if value < low or value > high:
                print(f"⚠️ {low}~{high} 사이의 숫자를 입력하세요.")
                continue
            return value

    def ask_yes_no(self, prompt):
        """y/n 확인을 받는다. 삭제처럼 되돌릴 수 없는 동작 직전에 쓴다."""
        while True:
            raw = input(prompt).strip().lower()
            if raw in ("y", "yes"):
                return True
            if raw in ("n", "no"):
                return False
            print("⚠️ y 또는 n 으로 답해주세요.")

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
        print("4. 퀴즈 삭제")
        print("5. 점수 확인")
        print("6. 기록 보기")
        print("7. 종료")
        print("=" * 40)

    # ─────────────────────────────────────────────────────────
    # 1. 퀴즈 풀기 (랜덤 출제 + 문제 수 선택 + 힌트)
    # ─────────────────────────────────────────────────────────
    def play(self):
        if not self.quizzes:      # 리스트가 비어있으면 (퀴즈가 하나도 없으면)
            print("\n등록된 퀴즈가 없습니다. 먼저 퀴즈를 추가하세요.")
            return

        total = len(self.quizzes)

        # [보너스 2] 몇 문제를 풀지 고른다. 1~등록된 문제 수 범위로 제한.
        print(f"\n📚 등록된 퀴즈는 총 {total}문제입니다.")
        count = self.ask_int(f"몇 문제를 풀까요? (1-{total}): ", 1, total)

        # [보너스 1] random.sample: 리스트에서 중복 없이 count개를 무작위로 뽑는다.
        #   - random.shuffle(리스트)  → 원본을 '제자리에서' 섞는다(반환값 None)
        #   - random.sample(리스트,k) → 원본은 그대로 두고 섞인 새 리스트를 반환
        # 여기서는 self.quizzes(원본 목록)를 건드리면 안 되고, 개수도 골라야 하므로
        # 섞기와 뽑기를 한 번에 해주는 sample이 정확히 맞는 도구다.
        selected = random.sample(self.quizzes, count)

        print(f"\n📝 퀴즈를 시작합니다! ({count}문제, 순서는 무작위)")
        print(f"   💡 정답 대신 '{HINT_KEY}'를 입력하면 힌트를 봅니다 "
              f"(맞혀도 {HINT_WEIGHT}문제만 인정)")

        score = 0          # 맞힌 문제 수 (표시용, 정수)
        earned = 0.0       # 실제 획득 점수 (힌트를 쓰면 0.5만 쌓인다)
        hint_used_count = 0   # 힌트를 본 문제 수
        deducted = 0.0        # 힌트 때문에 실제로 깎인 양(맞힌 문제만 해당)

        for i, quiz in enumerate(selected, start=1):
            print("\n" + "-" * 40)
            quiz.show(index=i)

            hint_used = False
            picked = None
            # 힌트를 봐도 아직 답을 고른 게 아니므로, 정답 번호가 나올 때까지 반복한다.
            while picked is None:
                value = self.ask_int(
                    f"정답 입력 (1-4, 힌트는 {HINT_KEY}): ", 1, 4,
                    hint_key=HINT_KEY,
                )
                if value == HINT_KEY:
                    if not quiz.has_hint():
                        print("⚠️ 이 문제에는 등록된 힌트가 없습니다.")
                        continue          # 힌트가 없으면 차감도 하지 않는다
                    print(f"💡 힌트: {quiz.hint}")
                    if not hint_used:     # 같은 문제에서 두 번 봐도 차감은 한 번만
                        hint_used = True
                        hint_used_count += 1
                    continue
                picked = value            # 숫자를 골랐으므로 반복 종료

            if quiz.is_correct(picked):
                score += 1
                if hint_used:
                    earned += HINT_WEIGHT
                    deducted += 1 - HINT_WEIGHT
                    print(f"✅ 정답입니다! (힌트 사용 → {HINT_WEIGHT}문제 인정)")
                else:
                    earned += 1
                    print("✅ 정답입니다!")
            else:
                print(f"❌ 오답입니다. 정답은 {quiz.answer}번.")

        # 점수 = 획득 점수를 100점 만점으로 환산 (힌트를 쓴 만큼 낮아진다)
        points = round(earned / count * 100)
        print("\n" + "=" * 40)
        print(f"🏆 결과: {count}문제 중 {score}문제 정답! ({points}점)")
        if hint_used_count:
            # 힌트를 봤어도 그 문제를 틀렸으면 깎일 점수 자체가 없다.
            # 그때 "0문제만큼 차감"이라고 찍으면 어색하므로 문구를 나눈다.
            # :g → 0.5는 '0.5', 1.0은 '1'로 깔끔하게 찍힌다.
            if deducted:
                print(f"💡 힌트 {hint_used_count}회 사용 "
                      f"(맞힌 문제에서 {deducted:g}문제만큼 차감)")
            else:
                print(f"💡 힌트 {hint_used_count}회 사용 (차감된 점수는 없음)")

        # [보너스 5] 최고 점수와 별개로, 이번 판의 기록을 모두 남긴다.
        self.history.append({
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "count": count,
            "correct": score,
            "hints": hint_used_count,
            "score": points,
        })

        # 최고점수 갱신 판단
        if points > self.best_score:
            self.best_score = points
            print("🎉 새로운 최고 점수입니다!")
        print("=" * 40)

        self.save()   # 점수·기록이 바뀌었으니 저장

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

        # [보너스 3] 힌트는 선택 사항이라 빈 입력을 허용한다(그냥 Enter = 힌트 없음).
        hint = input("힌트 (없으면 Enter): ").strip()

        # 새 Quiz 객체를 만들어 목록에 추가
        self.quizzes.append(Quiz(question, choices, answer, hint))
        self.save()
        print("✅ 퀴즈가 추가되었습니다!")

    # ─────────────────────────────────────────────────────────
    # 3. 퀴즈 목록
    # ─────────────────────────────────────────────────────────
    def list_quizzes(self):
        if not self.quizzes:
            print("\n등록된 퀴즈가 없습니다.")
            return
        print(f"\n📋 등록된 퀴즈 목록 (총 {len(self.quizzes)}개)")
        print("-" * 40)
        for i, quiz in enumerate(self.quizzes, start=1):
            mark = " 💡" if quiz.has_hint() else ""      # 힌트가 있는 문제 표시
            print(f"[{i}] {quiz.question}{mark}")
        print("-" * 40)

    # ─────────────────────────────────────────────────────────
    # 4. 퀴즈 삭제 (보너스 4)
    # ─────────────────────────────────────────────────────────
    def delete_quiz(self):
        if not self.quizzes:
            print("\n삭제할 퀴즈가 없습니다.")
            return

        self.list_quizzes()      # 어떤 번호를 지울지 보고 고르게 한다
        target = self.ask_int(
            f"삭제할 퀴즈 번호 (1-{len(self.quizzes)}, 취소는 0): ",
            0, len(self.quizzes),
        )
        if target == 0:
            print("삭제를 취소했습니다.")
            return

        # 화면 번호는 1부터, 리스트 인덱스는 0부터 → 1을 빼서 맞춘다.
        quiz = self.quizzes[target - 1]
        # 삭제는 되돌릴 수 없으므로 반드시 한 번 확인받는다.
        if not self.ask_yes_no(f"'{quiz.question}' 을(를) 삭제할까요? (y/n): "):
            print("삭제를 취소했습니다.")
            return

        # pop(i): i번째 원소를 리스트에서 빼내고 그 값을 돌려준다.
        removed = self.quizzes.pop(target - 1)
        self.save()              # 삭제 결과를 즉시 파일에 반영
        print(f"🗑️ 삭제했습니다: {removed.question}")

    # ─────────────────────────────────────────────────────────
    # 5. 점수 확인
    # ─────────────────────────────────────────────────────────
    def show_score(self):
        # 최고 점수가 0점이어도 플레이 기록은 있을 수 있다(0점만 받은 경우).
        # best_score만 보고 판단하면 "기록이 없습니다"라고 거짓말하게 된다.
        if self.best_score == 0 and not self.history:
            print("\n아직 퀴즈를 푼 기록이 없습니다.")
            return
        print(f"\n🏆 최고 점수: {self.best_score}점")
        if self.history:
            average = sum(r["score"] for r in self.history) / len(self.history)
            print(f"📊 플레이 {len(self.history)}회 · 평균 {average:.1f}점")

    # ─────────────────────────────────────────────────────────
    # 6. 기록 보기 (보너스 5)
    # ─────────────────────────────────────────────────────────
    def show_history(self, limit=10):
        if not self.history:
            print("\n아직 게임 기록이 없습니다.")
            return

        print(f"\n📜 게임 기록 (총 {len(self.history)}건)")
        if len(self.history) > limit:
            print(f"   최근 {limit}건만 표시합니다.")
        print("-" * 52)
        print(f"{'날짜/시간':<21}{'문제':>5}{'정답':>5}{'힌트':>5}{'점수':>7}")
        print("-" * 52)
        # 리스트[-limit:] → 뒤에서 limit개(=가장 최근 기록)만 잘라낸다.
        for r in self.history[-limit:]:
            # hints도 .get()으로 꺼낸다 — 힌트 횟수를 남기지 않던 기록이 섞여 있어도
            # KeyError로 죽지 않고 0으로 표시된다.
            print(f"{r['date']:<21}{r['count']:>5}{r['correct']:>5}"
                  f"{r.get('hints', 0):>5}{r['score']:>6}점")
        print("-" * 52)
        best = max(self.history, key=lambda record: record["score"])   # 점수가 가장 높은 기록
        print(f"🏆 최고 기록: {best['score']}점 ({best['date']})")

    # ─────────────────────────────────────────────────────────
    # 저장: Quiz 객체 → dict 로 바꿔 storage에 넘긴다
    # ─────────────────────────────────────────────────────────
    def save(self):
        raw = [q.to_dict() for q in self.quizzes]
        storage.save_state(raw, self.best_score, self.history)

    # ─────────────────────────────────────────────────────────
    # 메인 루프
    # ─────────────────────────────────────────────────────────
    def run(self):
        # KeyboardInterrupt(Ctrl+C), EOFError(입력 종료)에도 안전하게 종료
        try:
            while True:
                self.show_menu()
                choice = self.ask_int("선택: ", 1, 7)
                if choice == 1:
                    self.play()
                elif choice == 2:
                    self.add_quiz()
                elif choice == 3:
                    self.list_quizzes()
                elif choice == 4:
                    self.delete_quiz()
                elif choice == 5:
                    self.show_score()
                elif choice == 6:
                    self.show_history()
                elif choice == 7:
                    print("\n👋 게임을 종료합니다. 안녕히 가세요!")
                    self.save()
                    break
        except (KeyboardInterrupt, EOFError):
            # 비정상 종료 대신, 저장 후 깔끔하게 마무리
            print("\n\n⚠️ 입력이 중단되었습니다. 저장 후 종료합니다.")
            self.save()
