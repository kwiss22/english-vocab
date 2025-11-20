FROM python:3.11-slim

# 작업 디렉토리 설정
WORKDIR /app

# 시스템 의존성 설치
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Python 의존성 설치
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 애플리케이션 파일 복사
COPY web_vocab_app.py .
COPY templates/ templates/
COPY static/ static/
COPY vocabulary.json .
COPY quiz_stats.json .

# 포트 환경 변수 (Railway가 자동으로 설정)
# Railway는 PORT 환경 변수를 자동으로 설정하므로 ENV로 기본값만 설정
ENV PORT=5000

# 포트 노출 (동적 포트 사용)
EXPOSE 5000

# Gunicorn으로 Flask 앱 실행
# Railway의 PORT 환경 변수를 안전하게 처리
# exec form 대신 shell form을 사용하여 환경 변수 확장 보장
CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:${PORT:-5000} --workers 2 --threads 2 --timeout 120 web_vocab_app:app"]

