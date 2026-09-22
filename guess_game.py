"""数字を当てる数当てゲーム。難易度に応じて範囲が変わる。"""

import random

DIFFICULTIES = {
    "1": ("イージー", 1, 50),
    "2": ("ノーマル", 1, 100),
    "3": ("ハード", 1, 500),
}
HINT_THRESHOLDS = (5, 20)


def judge(guess: int, answer: int) -> str:
    if guess < answer:
        return "low"
    if guess > answer:
        return "high"
    return "correct"


def hint(guess: int, answer: int) -> str:
    distance = abs(guess - answer)
    if distance <= HINT_THRESHOLDS[0]:
        return "あと少し！"
    if distance <= HINT_THRESHOLDS[1]:
        return "近づいています。"
    return "まだ遠いです。"


def read_difficulty() -> tuple[str, int, int] | None:
    print("難易度を選んでください。")
    for key, (name, lower, upper) in DIFFICULTIES.items():
        print(f"  {key}: {name}（{lower}〜{upper}）")
    while True:
        try:
            choice = input("番号を入力してください: ").strip()
        except EOFError:
            return None
        if choice in DIFFICULTIES:
            return DIFFICULTIES[choice]
        print("1〜3の番号を入力してください。")


def read_guess(lower: int, upper: int) -> int | None:
    while True:
        try:
            raw = input(f"{lower}〜{upper}の数字を入力してください: ")
        except EOFError:
            return None
        try:
            guess = int(raw)
        except ValueError:
            print("数字を入力してください。")
            continue
        if not lower <= guess <= upper:
            print(f"{lower}〜{upper}の範囲で入力してください。")
            continue
        return guess


def play(answer: int | None = None, difficulty: tuple[str, int, int] | None = None) -> None:
    if difficulty is None:
        difficulty = read_difficulty()
        if difficulty is None:
            print("\n終了します。")
            return
    name, lower, upper = difficulty
    if answer is None:
        answer = random.randint(lower, upper)
    print(f"{name}モード: {lower}から{upper}までの数字を当ててください。")
    attempts = 0
    while True:
        guess = read_guess(lower, upper)
        if guess is None:
            print("\n終了します。")
            return
        attempts += 1
        result = judge(guess, answer)
        if result == "low":
            print("もっと大きい数字です。")
            print(hint(guess, answer))
        elif result == "high":
            print("もっと小さい数字です。")
            print(hint(guess, answer))
        else:
            print(f"正解です！ {attempts}回で当てました。")
            return


if __name__ == "__main__":
    play()
