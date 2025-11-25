#!/bin/sh
# Railway PORT 환경 변수 처리 스크립트

# PORT 환경 변수가 없으면 5000 사용
PORT=${PORT:-5000}

# Gunicorn 실행
exec gunicorn --bind 0.0.0.0:$PORT --workers 2 --threads 2 --timeout 120 web_vocab_app:app

