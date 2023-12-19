# 지하철 도착시간 Skill API

## 1. 설치 방법
```bash
# python venv 환경 활성화
$ python -m venv .venv
$ . .venv/bin/activate
(.venv)$ pip install -r requirements.txt
```

## 2. 실행 방법
```bash
# 지하철 도착시간 API키 환경변수 추가
# export SUBWAY_API_KEY=123456789abcdefg
$ export SUBWAY_API_KEY=<your-api-key>

# 단독으로 실행할 경우
$ uvicorn app.main:app --host 0.0.0.0 --reload --port 8080

# Nginx 리버스 프록시로 설정했을 경우
$ uvicorn app.main:app --reload --port 8080
```