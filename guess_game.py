"""数字を当てる数当てゲーム。難易度に応じて範囲が変わる。"""

import json
import random
from pathlib import Path

DIFFICULTIES = {
    "1": ("イージー", 1, 50),
    "2": ("ノーマル", 1, 100),
    "3": ("ハード", 1, 500),
}
SCORES_PATH = Path(__file__).resolve().parent / "high_scores.json"


def judge(guess: int, answer: int) -> str:
    if guess < answer:
        return "low"
    if guess > answer:
        return "high"
    return "correct"


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


def load_scores() -> dict[str, int]:
    try:
        with SCORES_PATH.open(encoding="utf-8") as scores_file:
            scores = json.load(scores_file)
    except (OSError, json.JSONDecodeError):
        return {}
    if not isinstance(scores, dict):
        return {}
    return {
        name: score
        for name, score in scores.items()
        if isinstance(name, str) and isinstance(score, int) and not isinstance(score, bool)
    }


def save_scores(scores: dict[str, int]) -> None:
    with SCORES_PATH.open("w", encoding="utf-8") as scores_file:
        json.dump(scores, scores_file, ensure_ascii=False, indent=2)
        scores_file.write("\n")


def update_best(
    scores: dict[str, int], difficulty_name: str, attempts: int
) -> tuple[dict[str, int], bool]:
    updated_scores = scores.copy()
    is_new_record = (
        difficulty_name not in updated_scores or attempts < updated_scores[difficulty_name]
    )
    if is_new_record:
        updated_scores[difficulty_name] = attempts
    return updated_scores, is_new_record


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
        elif result == "high":
            print("もっと小さい数字です。")
        else:
            print(f"正解です！ {attempts}回で当てました。")
            scores = load_scores()
            scores, is_new_record = update_best(scores, name, attempts)
            save_scores(scores)
            print(f"今回のスコア: {attempts}回")
            print(f"歴代ベストスコア: {scores[name]}回")
            if is_new_record:
                print("新記録です！")
            return


if __name__ == "__main__":
    play()
