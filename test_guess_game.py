"""guess_game のユニットテスト。"""

import json

import pytest

import guess_game


class TestJudge:
    def test_guess_below_answer_returns_low(self):
        assert guess_game.judge(10, 50) == "low"

    def test_guess_above_answer_returns_high(self):
        assert guess_game.judge(80, 50) == "high"

    def test_guess_equal_to_answer_returns_correct(self):
        assert guess_game.judge(50, 50) == "correct"


class TestHint:
    @pytest.mark.parametrize("distance", [0, 1, 4, 5])
    def test_distance_within_5(self, distance):
        assert guess_game.hint(50, 50 + distance) == "あと少し！"

    @pytest.mark.parametrize("distance", [6, 10, 19, 20])
    def test_distance_within_20(self, distance):
        assert guess_game.hint(50, 50 + distance) == "近づいています。"

    @pytest.mark.parametrize("distance", [21, 50, 100])
    def test_distance_over_20(self, distance):
        assert guess_game.hint(50, 50 + distance) == "まだ遠いです。"

    def test_negative_direction_uses_absolute_distance(self):
        assert guess_game.hint(50, 45) == "あと少し！"
        assert guess_game.hint(50, 30) == "近づいています。"
        assert guess_game.hint(50, 29) == "まだ遠いです。"


class TestUpdateBest:
    def test_new_difficulty_is_recorded(self):
        scores, is_new = guess_game.update_best({}, "ノーマル", 7)
        assert scores == {"ノーマル": 7}
        assert is_new is True

    def test_better_attempts_overwrites_existing_record(self):
        scores, is_new = guess_game.update_best({"ノーマル": 10}, "ノーマル", 5)
        assert scores == {"ノーマル": 5}
        assert is_new is True

    def test_worse_attempts_does_not_update(self):
        scores, is_new = guess_game.update_best({"ノーマル": 5}, "ノーマル", 8)
        assert scores == {"ノーマル": 5}
        assert is_new is False

    def test_equal_attempts_does_not_update(self):
        scores, is_new = guess_game.update_best({"ノーマル": 5}, "ノーマル", 5)
        assert scores == {"ノーマル": 5}
        assert is_new is False

    def test_other_difficulties_are_preserved(self):
        scores, _ = guess_game.update_best(
            {"イージー": 3, "ノーマル": 10}, "ノーマル", 4
        )
        assert scores == {"イージー": 3, "ノーマル": 4}

    def test_input_dict_is_not_mutated(self):
        original = {"ノーマル": 10}
        guess_game.update_best(original, "ノーマル", 4)
        assert original == {"ノーマル": 10}


class TestLoadScores:
    def test_missing_file_returns_empty_dict(self, tmp_path, monkeypatch):
        monkeypatch.setattr(guess_game, "SCORES_PATH", tmp_path / "missing.json")
        assert guess_game.load_scores() == {}

    def test_broken_json_returns_empty_dict(self, tmp_path, monkeypatch, capsys):
        scores_file = tmp_path / "high_scores.json"
        scores_file.write_text("{ not valid json", encoding="utf-8")
        monkeypatch.setattr(guess_game, "SCORES_PATH", scores_file)
        assert guess_game.load_scores() == {}
        assert "警告" in capsys.readouterr().out

    def test_valid_file_returns_scores(self, tmp_path, monkeypatch):
        scores_file = tmp_path / "high_scores.json"
        scores_file.write_text(
            json.dumps({"イージー": 3, "ノーマル": 7}), encoding="utf-8"
        )
        monkeypatch.setattr(guess_game, "SCORES_PATH", scores_file)
        assert guess_game.load_scores() == {"イージー": 3, "ノーマル": 7}

    def test_non_dict_json_returns_empty_dict(self, tmp_path, monkeypatch, capsys):
        scores_file = tmp_path / "high_scores.json"
        scores_file.write_text(json.dumps(["not", "a", "dict"]), encoding="utf-8")
        monkeypatch.setattr(guess_game, "SCORES_PATH", scores_file)
        assert guess_game.load_scores() == {}
        assert "警告" in capsys.readouterr().out


class TestSaveScores:
    def test_saves_scores_to_file(self, tmp_path, monkeypatch):
        scores_file = tmp_path / "high_scores.json"
        monkeypatch.setattr(guess_game, "SCORES_PATH", scores_file)
        assert guess_game.save_scores({"ノーマル": 5}) is True
        assert json.loads(scores_file.read_text(encoding="utf-8")) == {"ノーマル": 5}

    def test_unwritable_path_returns_false_and_warns(
        self, tmp_path, monkeypatch, capsys
    ):
        missing_dir_path = tmp_path / "no_such_dir" / "high_scores.json"
        monkeypatch.setattr(guess_game, "SCORES_PATH", missing_dir_path)
        assert guess_game.save_scores({"ノーマル": 5}) is False
        assert "警告" in capsys.readouterr().out
