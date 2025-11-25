# Railway 배포 에러 종합 해결 가이드

## 🔍 1단계: 에러 로그 확인

Railway 대시보드에서 정확한 에러 메시지를 확인하세요:

1. **Railway 대시보드 접속**
   - https://railway.app 접속
   - 프로젝트 선택
   - "Deployments" 탭 클릭
   - 최신 배포의 "View Logs" 클릭

2. **에러 메시지 복사**
   - 빨간색 에러 메시지 전체를 복사
   - 특히 다음 키워드 확인:
     - `Error:`
     - `Failed to`
     - `Cannot find`
     - `Port`
     - `Dockerfile`

## 🛠️ 2단계: 일반적인 에러 해결

### ❌ 에러 1: "Dockerfile not found" 또는 "Dockerfile `Dockerfile` does not exist"

**원인**: Railway가 Dockerfile을 찾지 못함

**해결 방법**:
1. 프로젝트 루트에 `Dockerfile` 파일이 있는지 확인 (대소문자 정확히)
2. `railway.json` 확인:
```json
{
  "build": {
    "builder": "DOCKERFILE",
    "dockerfilePath": "Dockerfile"
  }
}
```
3. GitHub에 파일이 올라갔는지 확인:
   ```bash
   git status
   git add Dockerfile
   git commit -m "Fix: Dockerfile 추가"
   git push
   ```

### ❌ 에러 2: "Error: '$PORT' is not a valid port number"

**원인**: PORT 환경 변수가 제대로 확장되지 않음

**해결 방법**:
1. `Dockerfile`의 CMD 확인:
```dockerfile
CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:${PORT:-5000} --workers 2 --threads 2 --timeout 120 web_vocab_app:app"]
```
2. Railway 대시보드에서 환경 변수 확인:
   - Settings → Variables
   - `PORT` 변수가 자동으로 설정되어 있는지 확인 (Railway가 자동 설정)

### ❌ 에러 3: "ModuleNotFoundError" 또는 "Import Error"

**원인**: requirements.txt에 패키지가 누락됨

**해결 방법**:
1. `requirements.txt` 확인:
```
Flask==3.0.0
Werkzeug==3.0.1
gunicorn==21.2.0
```
2. 로컬에서 테스트:
   ```bash
   pip install -r requirements.txt
   python web_vocab_app.py
   ```

### ❌ 에러 4: "FileNotFoundError: vocabulary.json"

**원인**: Dockerfile에서 파일 복사 누락

**해결 방법**:
1. `Dockerfile` 확인 - 다음 파일들이 모두 COPY되어야 함:
```dockerfile
COPY web_vocab_app.py .
COPY templates/ templates/
COPY static/ static/
COPY vocabulary.json .
COPY quiz_stats.json .
```

### ❌ 에러 5: "Connection refused" 또는 "502 Bad Gateway"

**원인**: 서버가 제대로 시작되지 않음

**해결 방법**:
1. `web_vocab_app.py`의 `start_server` 함수 확인:
   - `host='0.0.0.0'` 설정 확인
   - `port`가 `int(os.environ.get('PORT', 5000))`로 설정되어 있는지 확인
2. Railway 로그에서 "Starting gunicorn" 메시지 확인

## 🔧 3단계: 파일 확인 체크리스트

배포 전 다음 파일들이 모두 존재하고 올바른지 확인:

- [ ] `Dockerfile` (대소문자 정확히)
- [ ] `railway.json`
- [ ] `requirements.txt` (gunicorn 포함)
- [ ] `web_vocab_app.py`
- [ ] `templates/index.html`
- [ ] `static/style.css`
- [ ] `static/script.js`
- [ ] `vocabulary.json` (빈 파일이라도 있어야 함)
- [ ] `quiz_stats.json` (빈 파일이라도 있어야 함)

## 🚀 4단계: 재배포 방법

### 방법 1: 자동 재배포 (권장)
```bash
# 빈 커밋 생성하여 재배포 트리거
git commit --allow-empty -m "Trigger redeploy"
git push
```

### 방법 2: Railway 대시보드에서 재배포
1. Railway 대시보드 접속
2. 프로젝트 선택
3. "Deployments" 탭
4. 최신 배포 옆 "..." 메뉴 클릭
5. "Redeploy" 선택

### 방법 3: 수동 재배포
1. Railway 대시보드 접속
2. 프로젝트 선택
3. Settings → Source
4. "Redeploy" 버튼 클릭

## 📋 5단계: 최종 확인

배포가 성공하면:

1. **배포 상태 확인**
   - Railway 대시보드에서 "Deployed" 상태 확인
   - 초록색 체크 표시 확인

2. **서비스 URL 확인**
   - Settings → Domains
   - 생성된 URL 확인 (예: `https://your-app.railway.app`)

3. **실제 접속 테스트**
   - 브라우저에서 URL 접속
   - "영어 단어장 웹 애플리케이션" 제목 확인
   - 단어 추가/퀴즈 기능 테스트

## 🆘 여전히 문제가 있다면

1. **에러 로그 전체 복사**
   - Railway 로그에서 전체 에러 메시지 복사
   - 특히 빨간색 에러 부분

2. **GitHub 저장소 확인**
   - https://github.com/kwiss22/english-vocab
   - 모든 파일이 올라가 있는지 확인

3. **로컬 테스트**
   ```bash
   # Docker로 로컬 테스트
   docker build -t vocab-app .
   docker run -p 5000:5000 -e PORT=5000 vocab-app
   ```

## ✅ 현재 설정 확인

현재 프로젝트의 설정 상태:

- ✅ `Dockerfile` 존재 및 올바른 CMD 설정
- ✅ `railway.json`에 Dockerfile 빌더 설정
- ✅ `requirements.txt`에 gunicorn 포함
- ✅ `web_vocab_app.py`에서 PORT 환경 변수 처리
- ✅ `DOCKERFILE` (대문자) 파일 삭제 완료

---

**다음 단계**: Railway 대시보드에서 정확한 에러 메시지를 확인하고, 위의 해결 방법을 적용하세요.

