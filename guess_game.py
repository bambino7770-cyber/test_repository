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


def load_scores() -> dict[str, int]:
    try:
        with SCORES_PATH.open(encoding="utf-8") as scores_file:
            scores = json.load(scores_file)
    except FileNotFoundError:
        return {}
    except (OSError, ValueError) as error:
        print(f"警告: スコアを読み込めませんでした（{error}）。空の記録として続行します。")
        return {}
    if not isinstance(scores, dict):
        print("警告: スコアの形式が不正です。空の記録として続行します。")
        return {}
    return {
        name: score
        for name, score in scores.items()
        if isinstance(name, str) and isinstance(score, int) and not isinstance(score, bool)
    }


def save_scores(scores: dict[str, int]) -> bool:
    try:
        with SCORES_PATH.open("w", encoding="utf-8") as scores_file:
            json.dump(scores, scores_file, ensure_ascii=False, indent=2)
            scores_file.write("\n")
    except (OSError, TypeError, ValueError) as error:
        print(f"警告: スコアを保存できませんでした（{error}）。記録なしで続行します。")
        return False
    return True


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


def show_rankings(scores: dict[str, int]) -> None:
    if not scores:
        print("まだ記録がありません。")
        return
    print("== 歴代ベストスコア ==")
    for rank, (name, attempts) in enumerate(
        sorted(scores.items(), key=lambda item: item[1]), start=1
    ):
        print(f"  {rank}位: {name} {attempts}回")


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
            scores = load_scores()
            scores, is_new_record = update_best(scores, name, attempts)
            save_scores(scores)
            print(f"今回のスコア: {attempts}回")
            print(f"歴代ベストスコア: {scores[name]}回")
            if is_new_record:
                print("新記録です！")
            show_rankings(scores)
            return


if __name__ == "__main__":
    play()
