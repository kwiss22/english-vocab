#!/usr/bin/env python3
"""
Railway 배포용 실행 스크립트
PORT 환경 변수를 안전하게 처리하여 Gunicorn 실행
"""

import os
import sys
import subprocess

def get_port():
    """PORT 환경 변수를 안전하게 가져오기"""
    port_str = os.environ.get('PORT', '5000')
    
    # 문자열에서 숫자만 추출
    port_str_clean = ''.join(filter(str.isdigit, str(port_str)))
    
    if not port_str_clean:
        port_str_clean = '5000'
    
    try:
        port = int(port_str_clean)
        if port < 1 or port > 65535:
            print(f"Error: PORT {port} is out of range (1-65535)", file=sys.stderr)
            sys.exit(1)
        return port
    except ValueError:
        print(f"Error: Invalid PORT value: {port_str_clean}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    port = get_port()
    print(f"Starting Gunicorn on port {port}", flush=True)
    
    # Gunicorn을 subprocess로 실행 (더 안전함)
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

