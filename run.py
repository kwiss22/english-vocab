#!/usr/bin/env python3
"""
Railway 배포용 실행 스크립트
PORT 환경 변수를 안전하게 처리하여 Gunicorn 실행
"""

import os
import sys
import subprocess

# ✅ 올바른 방법: PORT 환경 변수를 직접 int()로 변환
port = int(os.environ.get("PORT", 5000))

if __name__ == '__main__':
    print(f"Starting Gunicorn on port {port}", flush=True)
    
    # Gunicorn 실행
    cmd = [
        'gunicorn',
        '--bind', f'0.0.0.0:{port}',
        '--workers', '2',
        '--threads', '2',
        '--timeout', '120',
        'web_vocab_app:app'
    ]
    
    print(f"Executing: {' '.join(cmd)}", flush=True)
    sys.exit(subprocess.call(cmd))

