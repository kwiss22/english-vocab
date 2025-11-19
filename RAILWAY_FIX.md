# Railway Next.js 에러 해결 가이드

## 🔧 문제 해결

Railway가 프로젝트를 Next.js로 잘못 인식하는 문제입니다.

## ✅ 해결 방법

### 방법 1: Railway 대시보드에서 수동 설정 (가장 확실함)

1. **Railway 대시보드 접속**
   - https://railway.app 접속
   - 프로젝트 선택

2. **Settings → Build & Deploy 설정**
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python web_vocab_app.py`
   - **Root Directory**: `.` (기본값)

3. **Service 설정**
   - Service → Settings → Source
   - **Nixpacks** 선택 (자동 감지 대신)

4. **재배포**
   - Deployments → "Redeploy" 클릭

---

### 방법 2: 새 서비스로 재생성

1. **기존 서비스 삭제** (선택사항)
   - Settings → Danger Zone → Delete Service

2. **새 서비스 생성**
   - "New" → "Empty Service"
   - GitHub 저장소 연결: `kwiss22/loveall`

3. **수동 설정**
   - Settings → Build & Deploy
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python web_vocab_app.py`

4. **환경 변수 설정** (선택사항)
   - Variables 탭
   - `FLASK_ENV=production` 추가

5. **배포**
   - "Deploy" 버튼 클릭

---

### 방법 3: 설정 파일 확인

생성된 파일들:
- ✅ `nixpacks.toml` - Nixpacks 빌드 설정
- ✅ `railway.json` - Railway 배포 설정
- ✅ `Procfile` - 프로세스 설정

이 파일들이 있으면 Railway가 자동으로 Flask 앱으로 인식해야 합니다.

---

## 🔍 확인 사항

### Railway 대시보드에서 확인:

1. **Settings → Build & Deploy**
   - Build Command가 올바른지 확인
   - Start Command가 올바른지 확인

2. **Deployments 탭**
   - 빌드 로그 확인
   - 에러 메시지 확인

3. **Logs 탭**
   - 실행 로그 확인
   - Flask 앱이 시작되는지 확인

---

## 📝 예상되는 정상 로그

배포가 성공하면 다음과 같은 로그가 보여야 합니다:

```
단어장 불러오기 성공: X개 단어
통계 불러오기 성공: X개 기록
영어 단어장 웹 애플리케이션 시작!
모드: 프로덕션
접속 주소: http://0.0.0.0:XXXX
```

---

## ❌ 여전히 Next.js 에러가 발생하면

1. **Railway 대시보드에서 명시적으로 설정**
   - Settings → Build & Deploy
   - 모든 명령어를 수동으로 입력

2. **서비스 재생성**
   - 완전히 새로 만들기

3. **다른 플랫폼 시도**
   - Render.com 사용 (Flask 지원 우수)

---

**문제가 계속되면 Railway 대시보드의 Build & Deploy 설정을 확인하세요!**

