import builtins
import re

import pytest

from v4_final import load_scores


@pytest.fixture
def make_csv(tmp_path):
    def write(content):
        path = tmp_path / "scores.csv"
        path.write_text(content, encoding="utf-8")
        return str(path)

    return write


def test_reads_valid_rows_in_order(make_csv):
    path = make_csv('name,score\n김하나,88\n"최,연성",77\n')
    assert load_scores(path) == ([("김하나", 88), ("최,연성", 77)], [])


def test_header_only_returns_empty_lists(make_csv):
    assert load_scores(make_csv("name,score\n")) == ([], [])


@pytest.mark.parametrize("content", ["", "score,name\n88,김하나\n", "name,grade\n"])
def test_missing_or_wrong_header(make_csv, content):
    with pytest.raises(ValueError, match="헤더|header|name,score"):
        load_scores(make_csv(content))


def test_missing_file(tmp_path):
    with pytest.raises(FileNotFoundError, match=r"missing\.csv"):
        load_scores(str(tmp_path / "missing.csv"))


def test_unreadable_file(make_csv, monkeypatch):
    path = make_csv("name,score\n")
    original_open = builtins.open

    def deny_scores_file(file, *args, **kwargs):
        if file == path:
            raise PermissionError("access denied")
        return original_open(file, *args, **kwargs)

    with monkeypatch.context() as patch:
        patch.setattr(builtins, "open", deny_scores_file)
        with pytest.raises(PermissionError, match="권한|denied"):
            load_scores(path)


@pytest.mark.parametrize(
    ("score_text", "expected_score", "reason"),
    [
        ("-1", None, "범위|정수"),
        ("0", 0, None),
        ("1", 1, None),
        ("99", 99, None),
        ("100", 100, None),
        ("101", None, "범위"),
    ],
)
def test_score_boundaries(make_csv, score_text, expected_score, reason):
    path = make_csv(f"name,score\n김하나,{score_text}\n")
    rows, errors = load_scores(path)

    if reason is None:
        assert rows == [("김하나", expected_score)]
        assert errors == []
    else:
        assert rows == []
        assert len(errors) == 1
        line_number, message = errors[0]
        assert line_number == 2
        assert re.search(reason, message)


def test_skips_invalid_rows_and_records_line_numbers_and_reasons(make_csv):
    path = make_csv(
        "name,score\n"
        "한칸\n"
        "세칸,80,추가\n"
        ",70\n"
        "빈점수,\n"
        "소수,82.5\n"
        "문자,abc\n"
        "정상,90\n"
    )

    rows, errors = load_scores(path)
    assert rows == [("정상", 90)]
    assert [line for line, _ in errors] == [2, 3, 4, 5, 6, 7]
    expected_reasons = ["열", "열", "이름", "점수", "정수", "정수"]
    for (_, message), expected in zip(errors, expected_reasons):
        assert expected in message


def test_duplicate_keeps_first_valid_score(make_csv):
    path = make_csv("name,score\n김하나,\n김하나,73\n김하나,95\n")
    rows, errors = load_scores(path)

    assert rows == [("김하나", 73)]
    assert [line for line, _ in errors] == [2, 4]
    assert "점수" in errors[0][1]
    assert "중복" in errors[1][1]
