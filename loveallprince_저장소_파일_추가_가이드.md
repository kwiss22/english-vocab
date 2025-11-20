# loveallprince/loveall 저장소에 영어 단어장 파일 추가 가이드

## 🔍 문제 확인

`loveallprince/loveall` 저장소에는:
- ❌ 영어 단어장 Flask 애플리케이션이 없음
- ✅ 테니스장 통합 플랫폼 (Next.js)만 있음

이것이 Railway 배포 실패의 원인입니다!

---

## ✅ 해결 방법: GitHub 웹에서 파일 추가

### 필수 파일 목록

다음 파일들을 `loveallprince/loveall` 저장소에 추가해야 합니다:

1. **Dockerfile** (배포용)
2. **requirements.txt** (Python 의존성)
3. **web_vocab_app.py** (Flask 애플리케이션)
4. **templates/index.html** (HTML 템플릿)
5. **static/style.css** (CSS)
6. **static/script.js** (JavaScript)
7. **vocabulary.json** (단어장 데이터)
8. **quiz_stats.json** (통계 데이터)

---

## 📝 단계별 추가 방법

### 1단계: GitHub 저장소 접속
1. https://github.com/loveallprince/loveall 접속
2. `loveallprince` 계정으로 로그인

### 2단계: Dockerfile 추가

1. **"Add file" → "Create new file"** 클릭
2. 파일명 입력: `Dockerfile`
3. 아래 내용 복사하여 붙여넣기:

```dockerfile
FROM python:3.11-slim

# 작업 디렉토리 설정
WORKDIR /app

# 시스템 의존성 설치
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Python 의존성 설치
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 애플리케이션 파일 복사
COPY web_vocab_app.py .
COPY templates/ templates/
COPY static/ static/
COPY vocabulary.json .
COPY quiz_stats.json .

# 포트 환경 변수 (Railway가 자동으로 설정)
ENV PORT=5000
EXPOSE $PORT

# Gunicorn으로 Flask 앱 실행 (환경 변수를 제대로 읽도록 쉘 사용)
CMD sh -c "gunicorn --bind 0.0.0.0:${PORT:-5000} --workers 2 --threads 2 --timeout 120 web_vocab_app:app"
```

4. **"Commit new file"** 클릭
   - 커밋 메시지: `Add Dockerfile for English vocab app`

---

### 3단계: requirements.txt 추가

1. **"Add file" → "Create new file"** 클릭
2. 파일명 입력: `requirements.txt`
3. 로컬 `requirements.txt` 파일 내용 복사하여 붙여넣기
4. **"Commit new file"** 클릭

---

### 4단계: web_vocab_app.py 추가

1. **"Add file" → "Create new file"** 클릭
2. 파일명 입력: `web_vocab_app.py`
3. 로컬 `web_vocab_app.py` 파일 내용 복사하여 붙여넣기
4. **"Commit new file"** 클릭

---

### 5단계: templates/index.html 추가

1. **"Add file" → "Create new file"** 클릭
2. 파일 경로 입력: `templates/index.html`
   - (파일명만 입력하면 루트에 생성됨, 경로를 입력하면 디렉토리 자동 생성)
3. 로컬 `templates/index.html` 파일 내용 복사하여 붙여넣기
4. **"Commit new file"** 클릭

---

### 6단계: static/style.css 추가

1. **"Add file" → "Create new file"** 클릭
2. 파일 경로 입력: `static/style.css`
3. 로컬 `static/style.css` 파일 내용 복사하여 붙여넣기
4. **"Commit new file"** 클릭

---

### 7단계: static/script.js 추가

1. **"Add file" → "Create new file"** 클릭
2. 파일 경로 입력: `static/script.js`
3. 로컬 `static/script.js` 파일 내용 복사하여 붙여넣기
4. **"Commit new file"** 클릭

---

### 8단계: vocabulary.json 추가

1. **"Add file" → "Create new file"** 클릭
2. 파일명 입력: `vocabulary.json`
3. 로컬 `vocabulary.json` 파일 내용 복사하여 붙여넣기
4. **"Commit new file"** 클릭

---

### 9단계: quiz_stats.json 추가

1. **"Add file" → "Create new file"** 클릭
2. 파일명 입력: `quiz_stats.json`
3. 로컬 `quiz_stats.json` 파일 내용 복사하여 붙여넣기
4. **"Commit new file"** 클릭

---

## 🚀 빠른 방법: ZIP 파일 업로드

파일이 많아서 하나씩 추가하기 어렵다면:

1. **로컬에서 필요한 파일들만 ZIP으로 압축**
2. **GitHub에서 "Upload files"** 클릭
3. **ZIP 파일 드래그 앤 드롭**
4. **커밋**

하지만 GitHub 웹에서는 ZIP 업로드가 직접 지원되지 않으므로, 파일을 하나씩 추가하는 것이 더 확실합니다.

---

## 📋 체크리스트

다음 파일들이 `loveallprince/loveall` 저장소에 있는지 확인:

- [ ] `Dockerfile`
- [ ] `requirements.txt`
- [ ] `web_vocab_app.py`
- [ ] `templates/index.html`
- [ ] `static/style.css`
- [ ] `static/script.js`
- [ ] `vocabulary.json`
- [ ] `quiz_stats.json`

---

## ✅ 파일 추가 후 확인

1. **Railway 대시보드 접속**
   - https://railway.app

2. **Deployments 탭 확인**
   - GitHub에 파일이 추가되면 자동으로 재배포 시작
   - 새로운 배포가 "Building" 상태로 시작됨

3. **빌드 로그 확인**
   - Dockerfile을 찾았다는 메시지 확인
   - 빌드가 성공적으로 진행되는지 확인

---

## 💡 팁

- 파일을 하나씩 추가하는 것이 가장 확실합니다
- 각 파일 추가 후 커밋하면 Railway가 자동으로 재배포를 시도합니다
- 모든 파일을 추가한 후 Railway에서 "Redeploy" 클릭하여 재배포

---

**모든 파일을 추가하면 Railway 배포가 성공합니다!** 🚀

