# Render 배포 가이드

## 🚀 Render로 배포하기

Render는 무료 플랜을 제공하며, GitHub와 연동하여 자동 배포가 가능합니다.

### 1단계: Render 계정 생성

1. https://render.com 접속
2. "Get Started for Free" 클릭
3. GitHub 계정으로 로그인

### 2단계: 프로젝트 배포

1. **"New +" → "Web Service" 선택**
   - GitHub 저장소 선택: `kwiss22/loveall`
   - 또는 저장소 연결

2. **설정**
   - **Name**: `loveall` (또는 원하는 이름)
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python web_vocab_app.py`
   - **Plan**: Free

3. **환경 변수 설정 (선택사항)**
   - Environment Variables 섹션
   - `FLASK_ENV=production` 추가 (선택사항)

4. **"Create Web Service" 클릭**

### 3단계: 도메인 확인

- Render가 자동으로 `.onrender.com` 도메인 제공
- Settings → Custom Domain에서 커스텀 도메인 추가 가능

### 4단계: 확인

- Render가 제공하는 URL로 접속
- 앱이 정상 작동하는지 확인

---

## 📝 배포 후 확인사항

- [ ] 앱이 정상적으로 로드되는가?
- [ ] 단어 추가/수정/삭제가 작동하는가?
- [ ] 퀴즈 기능이 작동하는가?
- [ ] 통계가 표시되는가?
- [ ] 다크 모드가 작동하는가?

---

## 🔄 업데이트 방법

코드를 수정한 후:

```bash
git add .
git commit -m "업데이트 내용"
git push
```

Render가 자동으로 재배포합니다.

---

## 💡 팁

- Render 무료 플랜: 서비스가 15분 동안 비활성화되면 슬리프 모드로 전환
- 첫 요청 시 약간의 지연이 있을 수 있음
- 데이터는 Render의 임시 스토리지에 저장됩니다
- 영구 저장이 필요하면 PostgreSQL 데이터베이스 추가 고려

---

**배포 완료!** 🎉

