# BLH Company 홈페이지

AI 기반 모빌리티 솔루션을 제공하는 BLH Company의 공식 홈페이지입니다.

## 🚀 주요 기능

### 📱 인스타그램 스타일 디자인
- **랜딩 페이지**: 동영상 배경과 3초 후 로고 애니메이션
- **공지사항**: 인스타그램 스타일 카드 레이아웃
- **이미지 업로드**: 공지사항에 이미지 첨부 기능

### 🎯 핵심 서비스
- **중고차 온라인 경매&공매**: C2B 온라인 경매 플랫폼
- **전기차 진단솔루션**: BLE 기반 OBD-II 진단기
- **자동차가격산정**: AI 기반 가격 산정 시스템
- **탁송물류관재시스템**: GPS 기반 실시간 위치 추적

### 🛠 관리자 기능
- **공지사항 관리**: CRUD 기능과 이미지 업로드
- **문의사항 관리**: 게시판 형식의 답변 시스템
- **대시보드**: 통계 정보 제공

## 🏗 기술 스택

### Backend
- **Python 3.11**
- **Flask 2.3.3**
- **SQLite** (개발/운영)
- **Gunicorn** (WSGI 서버)

### Frontend
- **HTML5** (시맨틱 마크업)
- **Tailwind CSS 3.4+** (유틸리티 기반)
- **JavaScript ES6+** (Vanilla JS)
- **Font Awesome 6.4.0**

### Infrastructure
- **Docker** + **Docker Compose**
- **Docker Hub**: `wecarmobility/blh-homepage`

## 🚀 실행 방법

### 로컬 실행
```bash
# 의존성 설치
pip install -r requirements.txt

# 애플리케이션 실행
python3 app.py

# 접속: http://localhost:3001
```

### Docker 실행
```bash
# Docker Hub에서 이미지 가져오기
docker pull wecarmobility/blh-homepage:latest

# 컨테이너 실행
docker run -d -p 3001:3001 --name blh-homepage wecarmobility/blh-homepage:latest

# 접속: http://localhost:3001
```

### Docker Compose 실행
```bash
# 컨테이너 시작
docker-compose up -d

# 접속: http://localhost:3001
```

## 🔐 관리자 접속

- **URL**: `/admin/login`
- **계정**: `bhl` / `bhl1004`

## 📁 프로젝트 구조

```
blh_hompage/
├── app.py                 # Flask 애플리케이션
├── requirements.txt       # Python 의존성
├── Dockerfile            # Docker 설정
├── docker-compose.yml    # Docker Compose 설정
├── static/               # 정적 파일
│   ├── css/
│   ├── js/
│   ├── images/
│   └── uploads/          # 업로드된 이미지
├── templates/            # HTML 템플릿
│   ├── admin/           # 관리자 페이지
│   └── *.html           # 공개 페이지
└── instance/            # SQLite 데이터베이스
```

## 🎨 페이지 구성

- **랜딩 페이지** (`/`): 동영상 배경 + 로고 애니메이션
- **홈페이지** (`/home`): 회사 개요 + 인터랙티브 서비스
- **회사소개** (`/about`): 사업 전략 + 매출 계획
- **서비스** (`/services`): 4가지 핵심 서비스 상세
- **문의하기** (`/contact`): 문의 폼 + FAQ
- **공지사항** (`/notices`): 인스타그램 스타일 그리드

## 🔧 API 엔드포인트

- **GET** `/health`: 헬스체크
- **POST** `/api/inquiry`: 문의하기
- **GET** `/api/company-info`: 회사 정보 조회

## 🌟 특징

### 반응형 디자인
- **Mobile First** 접근법
- **Tailwind CSS** 기반 유틸리티 클래스
- 모든 디바이스에서 최적화된 사용자 경험

### 인스타그램 스타일 UI
- 카드 형태의 공지사항 레이아웃
- 좋아요, 댓글, 공유 버튼
- 호버 애니메이션 효과

### 이미지 업로드 시스템
- 드래그 앤 드롭 업로드 영역
- 실시간 이미지 미리보기
- 파일 크기 및 형식 검증 (PNG, JPG, GIF, WebP, 최대 16MB)

## 📊 회사 정보

- **회사명**: 비엘에이치컴퍼니 주식회사 (BLH COMPANY)
- **대표자**: 홍독경
- **설립연도**: 2025년
- **주소**: 부산시 해운대 우동 1436 카이저빌 613호
- **전화**: 051-711-4929
- **이메일**: info@blhcompany.com

## 📈 사업 목표

- **2026년**: 40억원 매출 목표
- **2027년**: 107억원 매출 목표  
- **2028년**: 155억원 매출 목표

## 🔒 보안

- 세션 기반 관리자 인증
- 입력 검증 및 SQL 인젝션 방지
- 파일 업로드 보안 (secure_filename 사용)

## 📄 라이선스

© 2025 BLH Company. All rights reserved.
