#!/bin/sh
set -e

# Railway PORT 환경 변수 처리
# PORT가 설정되지 않았으면 5000 사용
if [ -z "$PORT" ]; then
    PORT=5000
fi

# PORT를 정수로 변환하여 확인
PORT=$(echo $PORT | sed 's/[^0-9]//g')
if [ -z "$PORT" ] || [ "$PORT" -lt 1 ] || [ "$PORT" -gt 65535 ]; then
    echo "Error: Invalid PORT value: $PORT"
    exit 1
fi

echo "Starting Gunicorn on port $PORT"

# Gunicorn 실행
exec gunicorn --bind 0.0.0.0:$PORT --workers 2 --threads 2 --timeout 120 web_vocab_app:app

