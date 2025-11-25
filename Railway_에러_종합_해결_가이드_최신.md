# Railway 에러 종합 해결 가이드 (최신)

## 🔍 현재 상태 확인

### 1단계: Railway 대시보드에서 에러 로그 확인

1. Railway 대시보드 접속: https://railway.app
2. 프로젝트 선택
3. **Deployments** 탭 클릭
4. 최신 배포의 **View Logs** 클릭
5. 에러 메시지 전체 복사

### 2단계: 일반적인 에러 유형별 해결

#### ❌ 에러 1: "COPY failed: file not found"
**원인**: Dockerfile에서 복사하려는 파일이 없음

**해결**:
```bash
# 로컬에서 파일 확인
ls -la vocabulary.json quiz_stats.json
```

**이미 해결됨**: Dockerfile이 파일이 없어도 작동하도록 수정됨

---

#### ❌ 에러 2: "Error: '$PORT' is not a valid port number"
**원인**: PORT 환경 변수가 제대로 확장되지 않음

**해결**: Dockerfile의 CMD가 올바른지 확인
```dockerfile
CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:${PORT:-5000} --workers 2 --threads 2 --timeout 120 web_vocab_app:app"]
```

**확인 사항**:
- Railway 대시보드 → **Variables** 탭에서 `PORT` 환경 변수가 자동 설정되어 있는지 확인
- 수동으로 설정하지 말 것 (Railway가 자동으로 설정)

---

#### ❌ 에러 3: "ModuleNotFoundError: No module named 'gunicorn'"
**원인**: requirements.txt에 gunicorn이 없거나 설치 실패

**해결**: requirements.txt 확인
```txt
Flask==3.0.0
Werkzeug==3.0.1
gunicorn==21.2.0
```

---

#### ❌ 에러 4: "Dockerfile not found" 또는 "Dockerfile `Dockerfile` does not exist"
**원인**: Dockerfile이 저장소에 없거나 경로가 잘못됨

**해결**:
1. GitHub 저장소에서 Dockerfile 존재 확인
2. `railway.json` 확인:
```json
{
  "build": {
    "builder": "DOCKERFILE",
    "dockerfilePath": "Dockerfile"
  }
}
```

---

#### ❌ 에러 5: "Application failed to respond"
**원인**: 앱이 시작되지 않음

**확인 사항**:
1. 로그에서 gunicorn 시작 메시지 확인
2. 포트 바인딩 확인
3. Flask 앱 로드 확인

---

## 🛠️ 즉시 해결 방법

### 방법 1: 파일 확인 및 커밋

```bash
# 1. 현재 파일 상태 확인
git status

# 2. 모든 변경사항 커밋
git add .
git commit -m "Fix: Railway 배포 에러 수정"

# 3. GitHub에 푸시
git push origin main
```

### 방법 2: Railway에서 재배포

1. Railway 대시보드 → **Deployments**
2. 최신 배포의 **⋯ (점 3개)** 클릭
3. **Redeploy** 선택

### 방법 3: Railway 설정 확인

1. **Settings** → **Build & Deploy**
2. **Builder**가 `DOCKERFILE`로 설정되어 있는지 확인
3. **Dockerfile Path**가 `Dockerfile`인지 확인

---

## 📋 체크리스트

배포 전 확인:

- [ ] `Dockerfile`이 프로젝트 루트에 있음
- [ ] `requirements.txt`에 `gunicorn==21.2.0` 포함
- [ ] `railway.json`에 `builder: "DOCKERFILE"` 설정
- [ ] `web_vocab_app.py`가 올바른 위치에 있음
- [ ] `templates/` 폴더가 있음
- [ ] `static/` 폴더가 있음
- [ ] 모든 파일이 GitHub에 푸시됨

---

## 🚀 최신 Dockerfile (확인용)

현재 Dockerfile은 다음 기능을 포함:

1. ✅ 파일이 없어도 빌드 성공 (vocabulary.json, quiz_stats.json)
2. ✅ PORT 환경 변수 안전 처리
3. ✅ Gunicorn으로 프로덕션 실행
4. ✅ Python 3.11 사용

---

## 💡 다음 단계

1. **에러 로그 확인**: Railway 대시보드에서 정확한 에러 메시지 확인
2. **에러 메시지 공유**: 에러 메시지를 알려주시면 구체적인 해결책 제공
3. **로컬 테스트**: Docker로 로컬에서 테스트
   ```bash
   docker build -t vocab-app .
   docker run -p 5000:5000 -e PORT=5000 vocab-app
   ```

---

## 📞 도움이 필요하시면

구체적인 에러 메시지를 알려주시면 더 정확한 해결책을 제공할 수 있습니다!

