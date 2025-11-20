# loveall 저장소 업로드 명령어

## 🎯 목표
`https://github.com/kwiss22/loveall` 저장소에 프로젝트 업로드

**현재 상태**: 저장소가 비어있음 ✅ (충돌 없이 업로드 가능)

---

## 📋 실행할 명령어 (순서대로)

### 1단계: Git 사용자 정보 설정 (필수!)

터미널에서 다음 명령어를 실행하세요:

```bash
git config --global user.name "kwiss22"
git config --global user.email "your-email@example.com"
```

**⚠️ 중요**: `your-email@example.com`을 실제 이메일 주소로 변경하세요!

### 2단계: 초기 커밋 생성

```bash
git commit -m "Initial commit: 영어 단어장 웹 애플리케이션"
```

### 3단계: loveall 저장소 연결

```bash
git remote add origin https://github.com/kwiss22/loveall.git
```

### 4단계: 브랜치 이름 변경

```bash
git branch -M main
```

### 5단계: GitHub에 업로드

```bash
git push -u origin main
```

---

## 🚀 전체 명령어 (한 번에 복사)

```bash
# 1. Git 사용자 정보 설정 (이메일을 실제 이메일로 변경!)
git config --global user.name "kwiss22"
git config --global user.email "your-email@example.com"

# 2. 초기 커밋 생성
git commit -m "Initial commit: 영어 단어장 웹 애플리케이션"

# 3. loveall 저장소 연결
git remote add origin https://github.com/kwiss22/loveall.git

# 4. 브랜치 이름 변경
git branch -M main

# 5. GitHub에 업로드
git push -u origin main
```

---

## ✅ 업로드 후 확인

1. https://github.com/kwiss22/loveall 접속
2. 파일 목록 확인
3. README.md가 표시되는지 확인

---

## ❓ 문제 해결

### 인증 오류 발생 시
- GitHub Personal Access Token 사용
- Settings → Developer settings → Personal access tokens → Generate new token
- 비밀번호 대신 토큰 사용

### 이미 원격 저장소가 연결된 경우
```bash
git remote remove origin
git remote add origin https://github.com/kwiss22/loveall.git
```

---

**위 명령어를 순서대로 실행하세요!** 🚀




