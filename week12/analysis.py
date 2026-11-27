import pandas as pd


def 정제(df):
    결과 = df.copy()
    print(f"원본: {len(결과)}행")

    # 점수가 비어 있는 행을 삭제한다.
    결과 = 결과.dropna(subset=["점수"])
    print(f"빈 점수 삭제 후: {len(결과)}행")

    # 모든 열이 같은 중복 행은 하나만 남긴다.
    결과 = 결과.drop_duplicates().copy()
    print(f"중복 삭제 후: {len(결과)}행")

    # 반과 과목의 앞뒤 공백을 제거한다.
    결과["반"] = 결과["반"].str.strip()
    결과["과목"] = 결과["과목"].str.strip()
    print(f"공백 제거 후: {len(결과)}행")

    # 0~100 사이의 정수 점수인 행만 남긴다.
    점수 = pd.to_numeric(결과["점수"], errors="coerce")
    유효 = 점수.between(0, 100) & (점수 % 1 == 0)
    결과 = 결과.loc[유효].copy()
    결과["점수"] = 점수.loc[유효].astype(int)
    print(f"점수 검증 후: {len(결과)}행")

    return 결과


def 반별평균(df):
    # 반별 통계 네 가지를 한 표로 계산한다.
    통계 = df.groupby("반")["점수"].agg(
        개수="count",
        평균="mean",
        중앙값="median",
        최댓값="max",
    ).round(2)

    print("\n[반별 통계]")
    print(통계)

    # 테스트에서 '1반' 같은 반 이름으로 평균을 꺼낼 수 있게 반환한다.
    return 통계["평균"].to_dict()


if __name__ == "__main__":
    원본 = pd.read_csv("scores_2026.csv", encoding="utf-8", dtype={"학번": str})
    정제된 = 정제(원본)

    수학 = 정제된[정제된["과목"] == "수학"]
    print(f"수학 데이터: {len(수학)}행")

    일반_고득점 = 정제된[(정제된["반"] == "1반") & (정제된["점수"] >= 90)]
    print(f"1반 90점 이상: {len(일반_고득점)}행")

    반별_평균 = 정제된.groupby("반")["점수"].mean().round(2)
    print("\n[반별 평균]")
    print(반별_평균)

    과목_반별_평균 = 정제된.groupby(["과목", "반"])["점수"].mean().round(2)
    print("\n[과목·반별 평균]")
    print(과목_반별_평균)

    반별평균(정제된)