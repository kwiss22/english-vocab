# Railway Dockerfile 에러 해결 가이드

## ❌ 에러: `Dockerfile 'Dockerfile' does not exist`

## 🔍 원인 확인

1. **GitHub 저장소 확인**
   - https://github.com/kwiss22/loveall 접속
   - 루트 디렉토리에 `Dockerfile` 파일이 있는지 확인
   - 파일이 보이면 ✅, 안 보이면 ❌

2. **Railway가 올바른 저장소를 보고 있는지 확인**
   - Railway 대시보드 → Settings → Source
   - 저장소가 `kwiss22/loveall`인지 확인
   - 브랜치가 `main`인지 확인

---

## ✅ 해결 방법

### 방법 1: Railway 대시보드에서 직접 설정 (가장 확실함)

1. **Railway 대시보드 접속**
   - https://railway.app
   - 프로젝트 선택

2. **Settings → Build & Deploy**
   - **Builder**: `Dockerfile` 선택
   - **Dockerfile Path**: `Dockerfile` 입력 (대소문자 구분!)
   - **Root Directory**: `.` (기본값, 루트 디렉토리)

3. **Source 설정 확인**
   - Settings → Source
   - **Repository**: `kwiss22/loveall` 확인
   - **Branch**: `main` 확인

4. **재배포**
   - Deployments → "Redeploy" 클릭

---

### 방법 2: GitHub에서 Dockerfile 확인

1. **GitHub 저장소 접속**
   - https://github.com/kwiss22/loveall

2. **Dockerfile 파일 확인**
   - 루트 디렉토리에 `Dockerfile` 파일이 있는지 확인
   - 파일이 없으면:
     - 로컬에서 `git add Dockerfile`
     - `git commit -m "Add Dockerfile"`
     - `git push`

---

### 방법 3: Railway 서비스 재생성

1. **기존 서비스 삭제** (선택사항)
   - Settings → Danger Zone → Delete Service

2. **새 서비스 생성**
   - "New" → "Empty Service"
   - GitHub 저장소 연결: `kwiss22/loveall`

3. **설정**
   - Settings → Build & Deploy
   - Builder: `Dockerfile`
   - Dockerfile Path: `Dockerfile`
   - Root Directory: `.`

4. **배포**
   - "Deploy" 버튼 클릭

---

## 🔧 추가 확인사항

### Dockerfile 경로 확인

Railway는 기본적으로 프로젝트 루트에서 Dockerfile을 찾습니다.

- ✅ 올바른 경로: `Dockerfile` (루트 디렉토리)
- ❌ 잘못된 경로: `./Dockerfile`, `Dockerfile/Dockerfile` 등

### Root Directory 확인

- Settings → Build & Deploy → Root Directory
- 값이 `.` 또는 비어있어야 함
- 다른 경로가 설정되어 있으면 `.`로 변경

---

## 📝 체크리스트

배포 전 확인:
- [ ] GitHub에 Dockerfile이 있는가?
- [ ] Railway가 올바른 저장소를 보고 있는가?
- [ ] Railway가 올바른 브랜치(main)를 보고 있는가?
- [ ] Builder가 Dockerfile로 설정되어 있는가?
- [ ] Dockerfile Path가 `Dockerfile`인가?
- [ ] Root Directory가 `.`인가?

---

## 🚀 빠른 해결

가장 빠른 해결 방법:

1. Railway 대시보드 → Settings → Build & Deploy
2. Builder: `Dockerfile` 선택
3. Dockerfile Path: `Dockerfile` 입력
4. Root Directory: `.` 확인
5. Save 클릭
6. Deployments → Redeploy 클릭

---

**설정 후 재배포하면 정상 작동할 것입니다!** 🎯

