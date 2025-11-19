# Railway 배포 가이드

## 🚀 Railway로 배포하기

Railway는 무료 플랜을 제공하며, GitHub와 연동하여 자동 배포가 가능합니다.

### 1단계: Railway 계정 생성

1. https://railway.app 접속
2. "Start a New Project" 클릭
3. GitHub 계정으로 로그인

### 2단계: 프로젝트 배포

1. **"Deploy from GitHub repo" 선택**
   - GitHub 저장소 선택: `kwiss22/loveall`
   - 또는 "New Project" → "Empty Project" 선택 후 GitHub 연결

2. **환경 변수 설정 (선택사항)**
   - Railway 대시보드 → Variables 탭
   - `FLASK_ENV=production` 추가 (선택사항)

3. **자동 배포**
   - GitHub에 푸시하면 자동으로 배포됩니다
   - 또는 Railway 대시보드에서 "Deploy" 버튼 클릭

### 3단계: 도메인 설정

1. Railway 대시보드 → Settings → Domains
2. "Generate Domain" 클릭하여 무료 도메인 생성
3. 또는 커스텀 도메인 추가

### 4단계: 확인

- Railway가 제공하는 URL로 접속
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

Railway가 자동으로 재배포합니다.

---

## 💡 팁

- Railway 무료 플랜: 월 500시간, $5 크레딧
- 데이터는 Railway의 임시 스토리지에 저장됩니다
- 영구 저장이 필요하면 데이터베이스 추가 고려

---

**배포 완료!** 🎉

