"""1〜100の数字を当てる数当てゲーム。"""

import random

LOWER = 1
UPPER = 100


def judge(guess: int, answer: int) -> str:
    if guess < answer:
        return "low"
    if guess > answer:
        return "high"
    return "correct"


def read_guess() -> int | None:
    try:
        raw = input(f"{LOWER}〜{UPPER}の数字を入力してください: ")
    except EOFError:
        return None
    try:
        guess = int(raw)
    except ValueError:
        print("数字を入力してください。")
        return read_guess()
    if not LOWER <= guess <= UPPER:
        print(f"{LOWER}〜{UPPER}の範囲で入力してください。")
        return read_guess()
    return guess


def play(answer: int | None = None) -> None:
    if answer is None:
        answer = random.randint(LOWER, UPPER)
    print(f"{LOWER}から{UPPER}までの数字を当ててください。")
    attempts = 0
    while True:
        guess = read_guess()
        if guess is None:
            print("\n終了します。")
            return
        attempts += 1
        result = judge(guess, answer)
        if result == "low":
            print("もっと大きい数字です。")
        elif result == "high":
            print("もっと小さい数字です。")
        else:
            print(f"正解です！ {attempts}回で当てました。")
            return


if __name__ == "__main__":
    play()
