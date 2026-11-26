import pytest

from load_scores import load_scores


@pytest.fixture
def csv_file(tmp_path):
    def write_csv(body):
        path = tmp_path / "scores.csv"
        path.write_text("name,score\n" + body, encoding="utf-8")
        return path

    return write_csv


def test_valid_rows_keep_order_and_duplicate_names(csv_file):
    path = csv_file('김하나,88\n"최,네번",77\n 김하나 , 91 \n')
    assert load_scores(path) == (
        [("김하나", 88), ("최,네번", 77), ("김하나", 91)],
        [],
    )


def test_header_only(csv_file):
    assert load_scores(csv_file("")) == ([], [])


def test_missing_file_raises(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_scores(tmp_path / "missing.csv")


@pytest.mark.parametrize("score", [0, 100])
def test_inclusive_score_boundaries(csv_file, score):
    assert load_scores(csv_file(f"A,{score}\n")) == ([("A", score)], [])


@pytest.mark.parametrize(
    ("row", "reason"),
    [
        ("A,-1", "점수가 0~100 밖"),
        ("A,101", "점수가 0~100 밖"),
        ("A", "열 개수가 2가 아님"),
        ("A,80,extra", "열 개수가 2가 아님"),
        (",90", "이름이 비어 있음"),
        ("A,", "점수가 비어 있음"),
        ("A,88.5", "점수가 정수가 아님"),
        ("A,abc", "점수가 정수가 아님"),
    ],
)
def test_invalid_row_is_logged_and_loading_continues(csv_file, row, reason):
    path = csv_file(f"\n{row}\nB,77\n")
    assert load_scores(path) == ([("B", 77)], [(3, row, reason)])
