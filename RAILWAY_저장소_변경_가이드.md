# Railway 저장소 변경 가이드

## 🔄 Railway에서 GitHub 저장소 변경하기

### 방법 1: 저장소 재연결 (추천)

#### 1단계: Railway 대시보드 접속
1. 브라우저에서 https://railway.app 접속
2. 로그인 (GitHub 계정)
3. 프로젝트 선택
   - 대시보드에서 `loveall` 또는 해당 프로젝트 클릭

---

#### 2단계: Settings 탭 열기
1. 왼쪽 사이드바에서 "Settings" 클릭
   - 또는 상단 메뉴에서 "Settings" 탭 클릭
2. Settings 페이지가 열림

---

#### 3단계: Source 섹션 찾기
1. Settings 페이지에서 "Source" 섹션 찾기
   - 페이지를 스크롤하여 찾기
   - 또는 왼쪽 사이드바의 "Source" 메뉴 클릭

---

#### 4단계: 현재 저장소 확인
1. "Source" 섹션에서 확인:
   - **Repository**: 현재 `loveallprince/loveall`로 표시됨
   - **Branch**: `main` (또는 다른 브랜치)
   - **Root Directory**: `.` (또는 다른 경로)

---

#### 5단계: 저장소 연결 해제
1. "Source" 섹션에서 "Disconnect" 버튼 찾기
   - Repository 옆에 있음
   - 또는 "..." (3점 메뉴) → "Disconnect" 선택
2. 확인 메시지가 나오면 "Disconnect" 또는 "확인" 클릭
3. 저장소 연결이 해제됨

---

#### 6단계: 새 저장소 연결
1. "Connect GitHub Repo" 버튼 클릭
   - 또는 "Connect Repository" 버튼
   - 빈 상태에서 나타나는 버튼

2. GitHub 저장소 선택
   - GitHub 저장소 목록이 표시됨
   - `kwiss22/loveall` 찾기
   - 클릭하여 선택

3. 브랜치 선택
   - Branch 드롭다운에서 `main` 선택
   - (기본값이 `main`일 수 있음)

4. Root Directory 확인
   - Root Directory: `.` (기본값)
   - 변경하지 않아도 됨

5. "Connect" 또는 "Save" 클릭
   - 저장소 연결 완료

---

#### 7단계: 자동 재배포 확인
1. 연결 후 자동으로 재배포가 시작됨
2. "Deployments" 탭으로 이동하여 확인
   - 새로운 배포가 "Building" 상태로 시작됨
3. 배포 완료 대기 (2-5분)

---

### 방법 2: 저장소 직접 변경 (일부 UI에서 가능)

일부 Railway UI에서는 저장소를 직접 변경할 수 있습니다:

1. **Settings → Source**
2. **Repository** 옆의 "Change" 또는 "Edit" 버튼 클릭
3. 새 저장소 선택: `kwiss22/loveall`
4. Branch: `main` 선택
5. "Save" 클릭

---

## 📋 변경 후 확인사항

### Settings → Source에서 확인:
- ✅ Repository: `kwiss22/loveall`
- ✅ Branch: `main`
- ✅ Root Directory: `.`

### Settings → Build & Deploy에서 확인:
- ✅ Builder: `Dockerfile`
- ✅ Dockerfile Path: `Dockerfile` (또는 비워두기)
- ✅ Root Directory: `.`

---

## 🔍 문제 해결

### "Disconnect" 버튼이 보이지 않으면:
1. Settings → Source에서
2. Repository 옆의 "..." (3점 메뉴) 클릭
3. "Disconnect" 또는 "Remove" 선택

### 저장소 목록에 `kwiss22/loveall`이 없으면:
1. GitHub에서 저장소 접근 권한 확인
2. Railway와 GitHub 계정이 올바르게 연결되었는지 확인
3. GitHub에서 Railway 앱 권한 확인

### 변경 후에도 에러가 발생하면:
1. Settings → Build & Deploy 확인
2. Builder가 `Dockerfile`인지 확인
3. Dockerfile Path가 올바른지 확인
4. Deployments → "Redeploy" 클릭

---

## ✅ 성공 확인

저장소 변경이 성공하면:
1. Settings → Source에서 Repository가 `kwiss22/loveall`로 표시됨
2. Deployments 탭에서 새로운 배포가 시작됨
3. 빌드 로그에 Dockerfile을 찾았다는 메시지가 나타남
4. 배포가 성공적으로 완료됨

---

## 💡 팁

- 저장소를 변경하면 자동으로 재배포가 시작됩니다
- 배포 중에는 설정을 변경하지 마세요
- 배포가 완료될 때까지 기다리세요 (보통 2-5분)

---

**저장소를 변경하면 Dockerfile을 찾을 수 있게 됩니다!** 🚀

