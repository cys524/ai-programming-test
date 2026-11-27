import pandas as pd

from analysis import 정제, 반별평균


# 각 CSV는 파일 맨 위에서 한 번씩만 읽고 정제한다.
전체 = 정제(pd.read_csv("scores_2026.csv", encoding="utf-8", dtype={"학번": str}))
미니 = 정제(pd.read_csv("mini.csv", encoding="utf-8", dtype={"학번": str}))


def test_정제후_100행():
    assert len(전체) == 100


def test_반_종류():
    assert set(전체["반"]) == {"1반", "2반"}


def test_반별_합계와_전체_합계():
    반별_합계 = 전체.groupby("반")["점수"].sum()
    assert 반별_합계.sum() == 전체["점수"].sum()


def test_미니_1반_평균():
    평균 = 반별평균(미니)
    assert 평균["1반"] == 80.0
    