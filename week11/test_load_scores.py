"""AI 도움을 받아 작성한 실습용 기준 테스트 초안."""
import pytest
from load_scores import load_scores


def test_scores_fixture():
    kept, skipped = load_scores("scores.csv")
    assert kept == [
        ("김하나", 88), ("최,네번", 77), ("김하나", 91),
        ("윤보람", 64), ("서한별", 95),
    ]
    assert [entry[0] for entry in skipped] == [3, 4, 7, 8, 9]


def test_empty_file():
    assert load_scores("empty.csv") == ([], [])


def test_missing_file(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_scores(tmp_path / "missing.csv")


def test_boundaries(tmp_path):
    path = tmp_path / "bounds.csv"
    path.write_text("name,score\nA,0\nB,100\nC,-1\nD,101\n", encoding="utf-8")
    kept, skipped = load_scores(path)
    assert kept == [("A", 0), ("B", 100)]
    assert skipped == [(4, "C,-1", "점수가 0~100 밖"), (5, "D,101", "점수가 0~100 밖")]


def test_invalid_rows(tmp_path):
    path = tmp_path / "invalid.csv"
    path.write_text("name,score\n,90\nB,\nC,88.5\nD,80,extra\n\n E , 77 \n", encoding="utf-8")
    kept, skipped = load_scores(path)
    assert kept == [("E", 77)]
    assert skipped == [
        (2, ",90", "이름이 비어 있음"),
        (3, "B,", "점수가 비어 있음"),
        (4, "C,88.5", "점수가 정수가 아님"),
        (5, "D,80,extra", "열 개수가 2가 아님"),
    ]


def test_same_name_with_both_boundary_scores(tmp_path):
    path = tmp_path / "same_name.csv"
    path.write_text("name,score\n김하나,0\n김하나,100\n", encoding="utf-8")
    assert load_scores(path) == ([("김하나", 0), ("김하나", 100)], [])
