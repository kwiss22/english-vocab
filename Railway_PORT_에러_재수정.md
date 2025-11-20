# Railway PORT 에러 재수정 가이드

## 🔴 문제

```
Error: '$PORT' is not a valid port number.
```

Railway가 `$PORT` 환경 변수를 제대로 인식하지 못하는 문제입니다.

---

## ✅ 해결 방법

### 수정된 파일들

1. **Dockerfile** ✅ (이미 수정됨)
   ```dockerfile
   CMD sh -c "gunicorn --bind 0.0.0.0:${PORT:-5000} --workers 2 --threads 2 --timeout 120 web_vocab_app:app"
   ```

2. **nixpacks.toml** ✅ (방금 수정)
   ```toml
   [start]
   cmd = "sh -c 'gunicorn --bind 0.0.0.0:${PORT:-5000} --workers 2 --threads 2 --timeout 120 web_vocab_app:app'"
   ```

3. **Procfile** ✅ (방금 수정)
   ```
   web: sh -c 'gunicorn -w 2 -b 0.0.0.0:${PORT:-5000} web_vocab_app:app'
   ```

---

## 🚀 다음 단계

### 1. 변경사항 푸시 완료 ✅

파일들이 이미 GitHub에 푸시되었습니다.

### 2. Railway에서 재배포

Railway는 자동으로 새로운 커밋을 감지하고 재배포를 시작합니다.

**수동 재배포 방법:**
1. Railway 대시보드 접속
2. 프로젝트 선택
3. **"Deployments"** 탭 클릭
4. **"Redeploy"** 버튼 클릭 (또는 최신 배포의 "..." 메뉴에서 "Redeploy")

### 3. 빌더 확인

Railway가 어떤 빌더를 사용하는지 확인:

1. 프로젝트 **Settings** 탭
2. **"Build & Deploy"** 섹션
3. **Builder** 확인:
   - `DOCKERFILE`로 설정되어 있는지 확인
   - 만약 `NIXPACKS`로 되어 있다면 `DOCKERFILE`로 변경

---

## 🔧 Railway 대시보드에서 빌더 설정

### 빌더를 Dockerfile로 명시적으로 설정

1. **Settings → Build & Deploy**
2. **Builder** 선택:
   - `DOCKERFILE` 선택
   - `Dockerfile Path`: `Dockerfile` (기본값)
3. **Save** 클릭

이렇게 하면 Railway가 항상 Dockerfile을 사용합니다.

---

## 📋 문제 해결 체크리스트

- [x] Dockerfile의 CMD 수정
- [x] nixpacks.toml의 cmd 수정
- [x] Procfile 수정
- [x] 변경사항 커밋 및 푸시
- [ ] Railway에서 재배포
- [ ] 빌더가 DOCKERFILE로 설정되어 있는지 확인
- [ ] 배포 로그에서 에러 없음 확인
- [ ] 배포 성공 확인

---

## 💡 왜 이 문제가 발생했나요?

Railway는 여러 설정 파일을 확인합니다:
1. `railway.json` / `railway.toml` (빌더 지정)
2. `Dockerfile` (Docker 빌더 사용 시)
3. `nixpacks.toml` (Nixpacks 빌더 사용 시)
4. `Procfile` (Heroku 스타일)

Railway가 자동으로 `nixpacks.toml`이나 `Procfile`을 감지하면, 이 파일들의 `$PORT` 변수가 제대로 확장되지 않을 수 있습니다.

**해결책:**
- 모든 설정 파일에서 `$PORT` 대신 `${PORT:-5000}` 사용
- `sh -c`를 사용하여 쉘에서 환경 변수 확장

---

## 🎯 지금 해야 할 일

1. **Railway 대시보드 접속**
2. **프로젝트 선택**
3. **Settings → Build & Deploy**에서 빌더 확인
4. **DOCKERFILE**로 설정되어 있는지 확인 (아니면 변경)
5. **Deployments** 탭에서 **"Redeploy"** 클릭
6. **배포 로그 확인**

---

**재배포 후에도 에러가 발생하면 배포 로그를 보내주세요!** 🚀

