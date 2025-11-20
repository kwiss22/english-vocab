# Railway 저장소 연결 가이드

## ✅ 현재 상황

- ✅ `kwiss22/english-vocab` 저장소 생성 완료
- ✅ 파일들이 이미 푸시되어 있음
- ⏭️ Railway에서 저장소 연결 필요

---

## 🚀 Railway 연결 방법

### 방법 1: kwiss22 계정으로 Railway 로그인 (권장)

`kwiss22/english-vocab` 저장소를 사용하려면 `kwiss22` 계정으로 Railway에 로그인해야 합니다.

#### 1단계: Railway 로그아웃
1. Railway 대시보드 접속: https://railway.app
2. 현재 로그인된 계정 확인
3. 로그아웃 (필요시)

#### 2단계: kwiss22 계정으로 로그인
1. Railway에서 **"Sign in with GitHub"** 클릭
2. `kwiss22` GitHub 계정으로 로그인
3. Railway가 `kwiss22` 계정의 저장소에 접근 가능

#### 3단계: 새 프로젝트 생성
1. **"New Project"** 클릭
2. **"GitHub Repo"** 선택
3. `kwiss22/english-vocab` 선택
4. Branch: `main` 선택
5. **"Deploy"** 클릭

---

### 방법 2: loveallprince 계정 사용 (저장소 변경 필요)

만약 `loveallprince` 계정으로 Railway를 계속 사용하고 싶다면:

#### 옵션 A: loveallprince 계정으로 새 저장소 생성
1. GitHub에서 `loveallprince/english-vocab` 저장소 생성
2. 로컬에서 새 저장소로 푸시
3. Railway에서 새 저장소 연결

#### 옵션 B: kwiss22 저장소에 협업자 추가
1. `kwiss22/english-vocab` 저장소 Settings → Collaborators
2. `loveallprince` 계정을 협업자로 추가
3. Railway에서 `kwiss22/english-vocab` 저장소 접근 가능

---

## 📋 단계별 실행

### 방법 1 실행 (kwiss22 계정 사용)

1. **Railway 로그아웃**
   - 현재 계정에서 로그아웃

2. **kwiss22 계정으로 로그인**
   - "Sign in with GitHub" 클릭
   - `kwiss22` 계정 선택

3. **새 프로젝트 생성**
   - "New Project" 클릭
   - "GitHub Repo" 선택
   - `kwiss22/english-vocab` 선택
   - "Deploy" 클릭

4. **배포 확인**
   - Deployments 탭에서 배포 상태 확인
   - Settings → Domains에서 URL 생성

---

## ✅ 확인 사항

### 저장소 확인
- [ ] `kwiss22/english-vocab` 저장소에 파일들이 있음
- [ ] Dockerfile이 있음
- [ ] requirements.txt가 있음
- [ ] web_vocab_app.py가 있음

### Railway 연결
- [ ] Railway에서 `kwiss22` 계정으로 로그인
- [ ] 새 프로젝트 생성
- [ ] `kwiss22/english-vocab` 저장소 선택
- [ ] 배포 시작

### 배포 확인
- [ ] Deployments에서 배포 상태 확인
- [ ] 빌드 로그에 에러 없음
- [ ] 배포 상태가 "Active"
- [ ] 서비스 URL 생성됨

---

## 💡 중요 사항

### 계정 일치
- Railway는 연결된 GitHub 계정의 저장소만 접근 가능
- `kwiss22/english-vocab` 저장소를 사용하려면 `kwiss22` 계정으로 Railway에 로그인해야 함

### 대안
- `loveallprince` 계정을 계속 사용하고 싶다면 `loveallprince/english-vocab` 저장소를 만들어야 함
- 또는 `kwiss22` 저장소에 `loveallprince`를 협업자로 추가

---

## 🎯 추천 방법

**`kwiss22` 계정으로 Railway에 로그인하는 것이 가장 간단합니다!**

이유:
- ✅ 저장소가 이미 생성되어 있음
- ✅ 파일들이 이미 푸시되어 있음
- ✅ 추가 작업 불필요

---

**지금 바로 Railway에서 `kwiss22` 계정으로 로그인하고 프로젝트를 생성하세요!** 🚀

