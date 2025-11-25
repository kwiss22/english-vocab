FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY web_vocab_app.py .
COPY templates/ ./templates/
COPY static/ ./static/

RUN echo '{}' > vocabulary.json && echo '{}' > quiz_stats.json

ENV PORT=5000
EXPOSE 5000

ENTRYPOINT ["/bin/sh", "-c"]
CMD ["PORT=${PORT:-5000} && exec gunicorn --bind 0.0.0.0:${PORT} --workers 2 --threads 2 --timeout 120 web_vocab_app:app"]