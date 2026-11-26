# 성적 CSV 검사 실습

## ① 무엇을 하나요
성적 CSV를 읽어 유효한 (이름, 점수) 목록과 제외한 행의 번호·내용·이유를 돌려줍니다.

## ② 왜 만들었나요
배포 CSV에는 빈 점수와 범위를 벗어난 점수가 섞여 있습니다. 점수가 0점 또는 100점일 때는 남기고, 빈 점수를 0점으로 바꾸거나 유효한 동명이인 기록을 빼지 않는지 확인하려고 테스트를 준비했습니다.

## ③ 어떻게 쓰나요
이 폴더를 VS Code로 연 다음 터미널에서 실행합니다.

```powershell
py -m pip install pytest pytest-cov
py load_scores.py scores.csv
```

## ④ 어떻게 테스트하나요
```powershell
py -m pytest test_load_scores.py --cov=load_scores --cov-report=term-missing
py -m pytest test_ai_A.py --cov=load_scores --cov-report=term-missing
py -m pytest test_ai_B.py --cov=load_scores --cov-report=term-missing
py -m pytest test_ai_bug.py
```

첫 번째 명령은 기준 테스트입니다. 아래 세 명령은 비교 실험이므로 하나씩 실행합니다.

## ⑤ 파일 구성

| 파일 | 하는 일 |
|---|---|
| load_scores.py, *.csv | 교수님 배포 프로그램과 입력 자료 |
| bug3_logic.py | 마지막 원소를 놓치는 함정 실험용 원본 |
| test_load_scores.py | AI 도움으로 작성한 기준 테스트 초안 |
| test_ai_A.py, test_ai_B.py, test_ai_bug.py | 각각 새 채팅에서 받은 원본 테스트 |
| find_max.py | 함정 테스트와 배포 함수의 모듈 이름을 연결 |
| comparison.md | 테스트 비교표 |

## ⑥ 만든 사람 · AI를 어디에 썼는지
- 작성자: 저장소 소유자
- AI 사용: 기준 테스트 초안, 새 채팅의 A/B/함정 테스트 생성, 실행과 결과 정리
- 추가 검증: AI 도움으로 같은 이름의 0점과 100점이 둘 다 유지되는 사례를 추가했습니다. 기준 테스트는 6개 모두 통과했습니다.

B 원본은 v4_final 모듈을 찾지 못합니다. 보충 실행 결과는 comparison.md에 정리했습니다. 함정 테스트는 원본을 그대로 두고 find_max.py를 통해 배포 함수에 연결했습니다. 실제 실행 결과는 6개 통과, 2개 실패였습니다.
