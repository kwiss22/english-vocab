#!/usr/bin/env python3
"""
Railway 배포용 실행 스크립트
PORT 환경 변수를 안전하게 처리하여 Gunicorn 실행
"""

import os
import sys

def get_port():
    """PORT 환경 변수를 안전하게 가져오기"""
    # 모든 환경 변수 출력 (디버깅용)
    print("Environment variables:", file=sys.stderr)
    for key, value in os.environ.items():
        if 'PORT' in key.upper():
            print(f"  {key}={value}", file=sys.stderr)
    
    port_str = os.environ.get('PORT')
    
    if not port_str:
        print("PORT environment variable not set, using default 5000", file=sys.stderr)
        port_str = '5000'
    else:
        print(f"PORT environment variable found: '{port_str}'", file=sys.stderr)
    
    # 문자열에서 숫자만 추출
    port_str_clean = ''.join(filter(str.isdigit, port_str))
    
    if not port_str_clean:
        print(f"Warning: Could not extract port number from '{port_str}', using default 5000", file=sys.stderr)
        port_str_clean = '5000'
    
    try:
        port = int(port_str_clean)
        if port < 1 or port > 65535:
            print(f"Error: PORT {port} is out of range (1-65535)", file=sys.stderr)
            sys.exit(1)
        print(f"Using port: {port}", file=sys.stderr)
        return port
    except ValueError:
        print(f"Error: Invalid PORT value: {port_str_clean}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    port = get_port()
    print(f"Starting Gunicorn on port {port}")
    
    # Gunicorn 실행
    os.execvp('gunicorn', [
        'gunicorn',
        '--bind', f'0.0.0.0:{port}',
        '--workers', '2',
        '--threads', '2',
        '--timeout', '120',
        'web_vocab_app:app'
    ])

