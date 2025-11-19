# Railway Dockerfile 설정 가이드

## 🚀 Railway 대시보드에서 Dockerfile 설정하기

### 1단계: Railway 대시보드 접속

1. **브라우저에서 Railway 접속**
   - https://railway.app 접속
   - GitHub 계정으로 로그인

2. **프로젝트 선택**
   - 대시보드에서 `loveall` 프로젝트 클릭
   - 또는 배포 중인 서비스 선택

---

### 2단계: 서비스 설정 열기

1. **서비스 선택**
   - 왼쪽 사이드바에서 서비스(Service) 클릭
   - 또는 메인 화면에서 서비스 카드 클릭

2. **Settings 탭 클릭**
   - 서비스 페이지 상단의 "Settings" 탭 클릭

---

### 3단계: Build & Deploy 설정

1. **Build & Deploy 섹션 찾기**
   - Settings 페이지에서 "Build & Deploy" 섹션 찾기
   - 스크롤 다운하여 찾기

2. **Builder 설정 변경**
   - **Builder** 드롭다운 메뉴 클릭
   - **"Dockerfile"** 선택
   - (기본값: "Nixpacks" 또는 "Automatic")

3. **Dockerfile Path 확인**
   - **Dockerfile Path** 입력란 확인
   - 값이 `Dockerfile`인지 확인 (기본값)
   - 다르면 `Dockerfile`로 변경

4. **Build Command 비우기**
   - **Build Command** 입력란을 **비워두기**
   - Dockerfile에서 빌드 명령어를 처리하므로 필요 없음

5. **Start Command 비우기**
   - **Start Command** 입력란을 **비워두기**
   - Dockerfile의 CMD에서 시작 명령어를 처리하므로 필요 없음

---

### 4단계: 설정 저장

1. **변경사항 저장**
   - 페이지 하단의 **"Save"** 또는 **"Update"** 버튼 클릭
   - 또는 변경사항이 자동 저장되는 경우 확인

---

### 5단계: 재배포

#### 방법 1: 수동 재배포
1. **Deployments 탭 클릭**
   - 상단 메뉴에서 "Deployments" 탭 클릭

2. **Redeploy 클릭**
   - 최신 배포 옆의 **"Redeploy"** 버튼 클릭
   - 또는 "..." 메뉴 → "Redeploy" 선택

#### 방법 2: GitHub 푸시로 자동 배포
- GitHub에 푸시하면 자동으로 재배포됩니다
- 이미 푸시했으므로 자동으로 시작될 수 있습니다

---

### 6단계: 배포 상태 확인

1. **Deployments 탭에서 확인**
   - 새로운 배포가 시작되었는지 확인
   - 상태가 "Building" 또는 "Deploying"인지 확인

2. **Logs 탭에서 확인**
   - "Logs" 탭 클릭
   - 빌드 로그 확인:
     ```
     Step 1/7 : FROM python:3.11-slim
     Step 2/7 : WORKDIR /app
     Step 3/7 : RUN apt-get update...
     Step 4/7 : COPY requirements.txt .
     Step 5/7 : RUN pip install...
     Step 6/7 : COPY . .
     Step 7/7 : CMD gunicorn...
     ```

3. **성공 확인**
   - 배포 상태가 "Active" 또는 "Running"이 되면 성공
   - 로그에 "Listening at: http://0.0.0.0:XXXX" 메시지 확인

---

## 📋 설정 요약

### 올바른 설정:
- **Builder**: `Dockerfile`
- **Dockerfile Path**: `Dockerfile`
- **Build Command**: (비워두기)
- **Start Command**: (비워두기)

### 잘못된 설정 (이전):
- **Builder**: `Nixpacks` 또는 `Automatic`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `python web_vocab_app.py`

---

## 🔍 문제 해결

### 여전히 Next.js 에러가 발생하면:

1. **Builder가 Dockerfile로 설정되었는지 확인**
   - Settings → Build & Deploy → Builder = `Dockerfile`

2. **Dockerfile이 루트 디렉토리에 있는지 확인**
   - GitHub 저장소에서 `Dockerfile` 파일이 있는지 확인

3. **캐시 삭제**
   - Settings → Advanced → "Clear Build Cache" 클릭
   - 재배포

4. **서비스 재생성**
   - 기존 서비스 삭제
   - 새 서비스 생성
   - GitHub 저장소 연결
   - Builder를 Dockerfile로 설정

---

## ✅ 성공 확인

배포가 성공하면:
- 배포 상태: "Active" 또는 "Running"
- 로그에 Flask 앱 시작 메시지
- 제공된 URL로 접속 가능
- 앱이 정상 작동

---

**설정 완료 후 재배포하면 정상 작동할 것입니다!** 🚀

