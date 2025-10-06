# 🚀 Vercel 배포 가이드

BLH Company 홈페이지를 Vercel에 배포하는 방법을 설명합니다.

## 📋 목차

1. [Vercel 배포 준비](#vercel-배포-준비)
2. [배포 과정](#배포-과정)
3. [환경 변수 설정](#환경-변수-설정)
4. [문제 해결](#문제-해결)
5. [제한사항 및 권장사항](#제한사항-및-권장사항)

## 🔧 Vercel 배포 준비

### 필수 파일들

다음 파일들이 프로젝트 루트에 있어야 합니다:

- ✅ `vercel.json` - Vercel 설정 파일
- ✅ `api/index.py` - Vercel용 Flask 애플리케이션
- ✅ `runtime.txt` - Python 버전 지정
- ✅ `requirements.txt` - Python 의존성
- ✅ `.vercelignore` - 배포 제외 파일

### 프로젝트 구조

```
blh_hompage/
├── api/
│   └── index.py          # Vercel용 Flask 앱
├── templates/            # HTML 템플릿
├── static/              # 정적 파일
├── vercel.json          # Vercel 설정
├── runtime.txt          # Python 버전
├── requirements.txt     # 의존성
└── .vercelignore       # 제외 파일
```

## 🚀 배포 과정

### 1. Vercel CLI 설치

```bash
# npm을 통한 설치
npm i -g vercel

# 또는 yarn을 통한 설치
yarn global add vercel
```

### 2. Vercel 로그인

```bash
vercel login
```

### 3. 프로젝트 배포

```bash
# 프로젝트 루트에서 실행
vercel

# 또는 프로덕션 배포
vercel --prod
```

### 4. 배포 설정

첫 배포 시 다음 질문들에 답변:

```
? Set up and deploy "blh_hompage"? [Y/n] Y
? Which scope do you want to deploy to? [your-username]
? Link to existing project? [y/N] N
? What's your project's name? blh-homepage
? In which directory is your code located? ./
```

## ⚙️ 환경 변수 설정

### Vercel Dashboard에서 설정

1. [Vercel Dashboard](https://vercel.com/dashboard) 접속
2. 프로젝트 선택
3. **Settings** → **Environment Variables**
4. 다음 변수들 추가:

| 변수명 | 값 | 설명 |
|--------|-----|------|
| `FLASK_ENV` | `production` | Flask 환경 |
| `SECRET_KEY` | `your-secret-key` | Flask 시크릿 키 |
| `DATABASE_URL` | `postgresql://...` | 데이터베이스 URL (선택) |

### CLI를 통한 설정

```bash
# 환경 변수 설정
vercel env add FLASK_ENV production
vercel env add SECRET_KEY your-secret-key-here

# 환경 변수 확인
vercel env ls
```

## 🔍 문제 해결

### 일반적인 오류들

#### 1. **Build 실패**

**증상**: `Build failed` 오류

**해결책**:
```bash
# requirements.txt 확인
cat requirements.txt

# Python 버전 확인
cat runtime.txt

# 로컬에서 테스트
python -m pip install -r requirements.txt
python api/index.py
```

#### 2. **Module Not Found**

**증상**: `ModuleNotFoundError: No module named 'flask'`

**해결책**:
```bash
# requirements.txt에 모든 의존성 포함 확인
pip freeze > requirements.txt

# 또는 수동으로 추가
echo "Flask==2.3.3" >> requirements.txt
echo "Flask-SQLAlchemy==3.0.5" >> requirements.txt
```

#### 3. **Template Not Found**

**증상**: `TemplateNotFound: landing.html`

**해결책**:
```python
# api/index.py에서 템플릿 폴더 경로 확인
app = Flask(__name__, template_folder='../templates', static_folder='../static')
```

#### 4. **Database 오류**

**증상**: SQLite 관련 오류

**해결책**:
- Vercel은 서버리스 환경이므로 SQLite 제한적
- PostgreSQL이나 PlanetScale 사용 권장

```python
# 프로덕션용 데이터베이스 설정
import os

if os.environ.get('DATABASE_URL'):
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tmp/blh_company.db'
```

### 로그 확인

```bash
# 배포 로그 확인
vercel logs [deployment-url]

# 실시간 로그
vercel logs --follow
```

## ⚠️ 제한사항 및 권장사항

### Vercel 제한사항

1. **서버리스 환경**
   - 각 요청은 독립적으로 처리
   - 파일 시스템 쓰기 제한 (`/tmp`만 가능)
   - 실행 시간 제한 (Hobby: 10초, Pro: 60초)

2. **데이터베이스**
   - SQLite는 임시 저장소에만 저장 가능
   - 데이터 영속성 보장 안됨
   - 외부 데이터베이스 사용 권장

3. **파일 업로드**
   - 로컬 파일 시스템 사용 불가
   - AWS S3, Cloudinary 등 클라우드 스토리지 필요

### 권장사항

#### 1. **데이터베이스 마이그레이션**

**PlanetScale (MySQL) 사용**:
```bash
# PlanetScale CLI 설치
npm install -g @planetscale/cli

# 데이터베이스 생성
pscale database create blh-company

# 연결 문자열 가져오기
pscale connect blh-company main
```

**Supabase (PostgreSQL) 사용**:
```python
# requirements.txt에 추가
psycopg2-binary==2.9.7

# 환경 변수 설정
DATABASE_URL=postgresql://user:pass@host:port/dbname
```

#### 2. **파일 업로드 개선**

**Cloudinary 사용**:
```python
import cloudinary
import cloudinary.uploader

# 설정
cloudinary.config(
    cloud_name="your-cloud-name",
    api_key="your-api-key",
    api_secret="your-api-secret"
)

# 업로드
result = cloudinary.uploader.upload(file)
image_url = result['secure_url']
```

#### 3. **성능 최적화**

```python
# 캐싱 추가
from flask_caching import Cache

cache = Cache(app, config={'CACHE_TYPE': 'simple'})

@app.route('/api/company-info')
@cache.cached(timeout=300)  # 5분 캐시
def api_company_info():
    # ...
```

## 📊 배포 후 확인사항

### 1. **기본 기능 테스트**

```bash
# 헬스체크
curl https://your-app.vercel.app/health

# 메인 페이지
curl https://your-app.vercel.app/

# API 테스트
curl https://your-app.vercel.app/api/test
```

### 2. **성능 모니터링**

- Vercel Analytics 활성화
- 응답 시간 모니터링
- 오류 로그 확인

### 3. **도메인 설정**

```bash
# 커스텀 도메인 추가
vercel domains add your-domain.com

# DNS 설정 확인
vercel domains inspect your-domain.com
```

## 🔄 지속적 배포

### GitHub 연동

1. Vercel Dashboard에서 GitHub 연동
2. Repository 선택
3. 자동 배포 설정

### 배포 트리거

- `main` 브랜치 푸시 시 자동 배포
- Pull Request 시 프리뷰 배포
- 수동 배포도 가능

## 📞 지원

배포 중 문제가 발생하면:

1. **Vercel 문서**: https://vercel.com/docs
2. **커뮤니티**: https://github.com/vercel/vercel/discussions
3. **로그 분석**: `vercel logs` 명령어 활용

---

## 🎯 빠른 배포 체크리스트

- [ ] `vercel.json` 파일 생성
- [ ] `api/index.py` 파일 생성
- [ ] `runtime.txt` 파일 생성
- [ ] `requirements.txt` 업데이트
- [ ] `.vercelignore` 파일 생성
- [ ] Vercel CLI 설치 및 로그인
- [ ] `vercel` 명령어로 배포
- [ ] 환경 변수 설정
- [ ] 배포 확인 및 테스트

**🎉 성공적인 Vercel 배포를 위해 이 가이드를 따라해보세요!**
