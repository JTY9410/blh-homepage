from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
import sqlite3
import json
from werkzeug.utils import secure_filename

app = Flask(__name__, template_folder='../templates', static_folder='../static', instance_relative_config=False)
app.config['SECRET_KEY'] = 'blh-company-secret-key-2025'

# Vercel용 데이터베이스 설정 (SQLite는 서버리스에서 제한적)
# 프로덕션에서는 PostgreSQL이나 MySQL 사용 권장
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/blh_company.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.instance_path = '/tmp'

# 이미지 업로드 설정 (Vercel에서는 임시 저장소 사용)
app.config['UPLOAD_FOLDER'] = '/tmp/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB 제한
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# 업로드 폴더 생성
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

db = SQLAlchemy(app)

# Database Models
class Notice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(100), default='관리자')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    priority = db.Column(db.Integer, default=0)  # 0: 일반, 1: 중요
    is_published = db.Column(db.Boolean, default=True)
    view_count = db.Column(db.Integer, default=0)
    image_url = db.Column(db.String(500))  # 이미지 URL 필드 추가

class Inquiry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20))
    company = db.Column(db.String(100))
    service_interest = db.Column(db.String(100))
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_processed = db.Column(db.Boolean, default=False)
    is_public = db.Column(db.Boolean, default=True)

class InquiryAnswer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    inquiry_id = db.Column(db.Integer, db.ForeignKey('inquiry.id'), nullable=False)
    answer = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    inquiry = db.relationship('Inquiry', backref=db.backref('answers', lazy=True))

# Routes
@app.route('/')
def landing():
    """랜딩 페이지"""
    return render_template('landing.html')

@app.route('/home')
def home():
    """홈페이지"""
    try:
        latest_notices = Notice.query.filter_by(is_published=True).order_by(Notice.priority.desc(), Notice.created_at.desc()).limit(3).all()
    except:
        latest_notices = []
    return render_template('home.html', latest_notices=latest_notices)

@app.route('/landing')
def landing_alias():
    """랜딩 페이지 별칭"""
    return redirect(url_for('landing'))

@app.route('/services')
def services():
    """서비스 소개"""
    return render_template('services.html')

@app.route('/about')
def about():
    """회사소개"""
    return render_template('about.html')

@app.route('/contact')
def contact():
    """문의하기"""
    return render_template('contact.html')

@app.route('/notices')
def notices():
    """공지사항 목록"""
    try:
        notices = Notice.query.filter_by(is_published=True).order_by(Notice.priority.desc(), Notice.created_at.desc()).all()
    except:
        notices = []
    return render_template('notices.html', notices=notices)

@app.route('/notices/<int:notice_id>')
def notice_detail(notice_id):
    """공지사항 상세"""
    try:
        notice = Notice.query.get_or_404(notice_id)
        # 조회수 증가
        notice.view_count += 1
        db.session.commit()
    except:
        notice = None
    
    if not notice:
        return render_template('404.html'), 404
    
    return render_template('notice_detail.html', notice=notice)

@app.route('/health')
def health():
    """헬스체크"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'version': '1.0.0'
    })

@app.route('/api/test')
def api_test():
    """API 테스트"""
    return jsonify({
        'message': 'BLH Company API is working!',
        'timestamp': datetime.utcnow().isoformat()
    })

@app.route('/api/inquiry', methods=['POST'])
def api_inquiry():
    """문의 접수 API"""
    try:
        data = request.get_json()
        
        inquiry = Inquiry(
            name=data.get('name'),
            email=data.get('email'),
            phone=data.get('phone', ''),
            company=data.get('company', ''),
            service_interest=data.get('service_interest', ''),
            message=data.get('message')
        )
        
        db.session.add(inquiry)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': '문의가 성공적으로 접수되었습니다.',
            'inquiry_id': inquiry.id
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': '문의 접수 중 오류가 발생했습니다.',
            'error': str(e)
        }), 500

@app.route('/api/company-info')
def api_company_info():
    """회사 정보 API"""
    return jsonify({
        'company_name': 'BLH Company',
        'description': 'AI 기반 모빌리티 솔루션으로 투명하고 효율적인 중고차 거래',
        'address': '부산시 해운대 우동 1436 카이저빌 613호',
        'phone': '051-711-4929',
        'email': 'info@blhcompany.com',
        'business_hours': '평일 09:00-18:00',
        'services': [
            '온라인 경매 및 공매 운영',
            'EV 진단 활성화 및 사전 고장 진단 플랫폼',
            '빅데이터 기반 가격 산정 시스템',
            '탁송 관재시스템 및 ERP'
        ]
    })

# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

# Initialize database (Vercel 환경에서 안전하게)
def init_db():
    try:
        with app.app_context():
            db.create_all()
            return True
    except Exception as e:
        print(f"Database initialization error: {e}")
        return False

# 데이터베이스 초기화 상태 추적
_db_initialized = False

def ensure_db_initialized():
    global _db_initialized
    if not _db_initialized:
        _db_initialized = init_db()
    return _db_initialized

# 모든 데이터베이스 관련 라우트에서 초기화 확인
@app.before_request
def before_request():
    if request.endpoint and any(endpoint in request.endpoint for endpoint in ['home', 'notices', 'notice_detail', 'api_inquiry']):
        ensure_db_initialized()

# Vercel handler
def handler(request):
    return app(request.environ, request.start_response)

if __name__ == '__main__':
    app.run(debug=False)
