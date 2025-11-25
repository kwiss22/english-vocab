# Railway PORT 에러 최종 해결 방법

## 🔴 문제

```
Error: '$PORT' is not a valid port number.
```

Railway가 `$PORT` 환경 변수를 문자열로 인식하는 문제입니다.

---

## ✅ 해결 방법

### 1. Dockerfile만 사용하도록 설정 정리

다른 설정 파일(`nixpacks.toml`, `Procfile`)이 Railway의 빌더 선택을 방해할 수 있으므로 백업 처리했습니다.

**변경 사항:**
- ✅ `nixpacks.toml` → `nixpacks.toml.bak` (백업)
- ✅ `Procfile` → `Procfile.bak` (백업)
- ✅ `Dockerfile` CMD 명령어 개선

### 2. Dockerfile CMD 수정

```dockerfile
# ✅ 올바른 방식: exec form 사용
CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:${PORT:-5000} --workers 2 --threads 2 --timeout 120 web_vocab_app:app"]
```

**핵심 포인트:**
- `sh -c`를 사용하여 쉘에서 환경 변수 확장
- `${PORT:-5000}` 형식으로 기본값 제공
- exec form `["sh", "-c", "..."]` 사용

---

## 🚀 다음 단계

### 1. Railway 대시보드에서 빌더 확인

1. **Railway 대시보드 접속**
   - https://railway.app

2. **프로젝트 선택**

3. **Settings → Build & Deploy**
   - **Builder**: `DOCKERFILE` 확인
   - **Dockerfile Path**: `Dockerfile` 확인
   - 만약 `NIXPACKS`로 되어 있다면 `DOCKERFILE`로 변경

### 2. 재배포

1. **Deployments 탭** 클릭
2. **"Redeploy"** 버튼 클릭
   - 또는 최신 배포의 "..." 메뉴 → "Redeploy"

### 3. 배포 로그 확인

배포 로그에서 다음을 확인:
- ✅ `$PORT` 에러가 사라졌는지
- ✅ 빌드가 성공적으로 완료되는지
- ✅ 컨테이너가 정상적으로 시작되는지

---

## 🔧 Railway 대시보드에서 수동 설정

### 빌더를 DOCKERFILE로 강제 설정

1. **Settings → Build & Deploy**
2. **Builder** 드롭다운에서 `DOCKERFILE` 선택
3. **Dockerfile Path**: `Dockerfile` 확인
4. **Save** 클릭

### 환경 변수 확인 (선택사항)

Railway가 PORT 환경 변수를 자동으로 설정하지만, 확인하려면:

1. **Settings → Variables**
2. `PORT` 변수가 있는지 확인 (없어도 됨 - Railway가 자동 설정)
3. 만약 수동으로 설정하려면:
   - **New Variable**
   - **Name**: `PORT`
   - **Value**: (비워두기 - Railway가 자동으로 할당)

---

## 📋 문제 해결 체크리스트

### 코드 수정
- [x] Dockerfile CMD 수정 (exec form 사용)
- [x] nixpacks.toml 백업 처리
- [x] Procfile 백업 처리
- [x] railway.json/railway.toml에서 DOCKERFILE 명시

### Railway 설정
- [ ] Settings → Build & Deploy에서 Builder가 DOCKERFILE인지 확인
- [ ] Dockerfile Path가 `Dockerfile`인지 확인
- [ ] 재배포 실행

### 배포 확인
- [ ] 배포 로그에 `$PORT` 에러 없음
- [ ] 빌드 성공
- [ ] 컨테이너 시작 성공
- [ ] 배포 상태 "Active"
- [ ] 웹앱 접속 가능

---

## 💡 왜 이 방법이 작동하나요?

### 문제 원인
1. Railway가 여러 설정 파일을 자동 감지
2. `nixpacks.toml`이나 `Procfile`이 우선순위를 가질 수 있음
3. 이 파일들의 `$PORT` 처리가 제대로 작동하지 않음

### 해결 방법
1. **Dockerfile만 사용**: 다른 설정 파일을 백업 처리
2. **railway.json/railway.toml에서 명시**: 빌더를 `DOCKERFILE`로 명시
3. **Dockerfile CMD 개선**: exec form과 쉘 확장 사용

---

## 🎯 지금 바로 해야 할 일

1. **Railway 대시보드 접속**
2. **Settings → Build & Deploy** 확인
   - Builder: `DOCKERFILE`
   - Dockerfile Path: `Dockerfile`
3. **Deployments → Redeploy** 클릭
4. **배포 로그 확인**

---

## ⚠️ 여전히 에러가 발생한다면

1. **배포 로그 전체 복사**
2. **Railway Settings → Build & Deploy 스크린샷**
3. **에러 메시지와 함께 알려주세요**

---

**재배포 후 결과를 알려주세요!** 🚀


