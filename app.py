from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
import sqlite3
import json
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SECRET_KEY'] = 'blh-company-secret-key-2025'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blh_company.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 이미지 업로드 설정
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB 제한
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# 업로드 폴더 생성
os.makedirs(os.path.join(app.root_path, app.config['UPLOAD_FOLDER']), exist_ok=True)

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
    admin_name = db.Column(db.String(100), default='관리자')
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Routes
@app.route('/')
def landing():
    """랜딩 페이지"""
    return render_template('landing.html')

@app.route('/home')
def home():
    """홈페이지"""
    latest_notices = Notice.query.filter_by(is_published=True).order_by(Notice.priority.desc(), Notice.created_at.desc()).limit(3).all()
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
    """회사 소개"""
    return render_template('about.html')

@app.route('/contact')
def contact():
    """문의하기"""
    public_inquiries = Inquiry.query.filter_by(is_public=True).order_by(Inquiry.created_at.desc()).all()
    # Fetch answers grouped by inquiry_id
    answers_by_inquiry = {}
    answer_rows = InquiryAnswer.query.order_by(InquiryAnswer.created_at.asc()).all()
    for ans in answer_rows:
        answers_by_inquiry.setdefault(ans.inquiry_id, []).append(ans)
    return render_template('contact.html', inquiries=public_inquiries, answers_by_inquiry=answers_by_inquiry)

@app.route('/notices')
def notices():
    """공지사항 목록"""
    notices_list = Notice.query.filter_by(is_published=True).order_by(Notice.priority.desc(), Notice.created_at.desc()).all()
    return render_template('notices.html', notices=notices_list)

@app.route('/notices/<int:notice_id>')
def notice_detail(notice_id):
    """공지사항 상세"""
    notice = Notice.query.get_or_404(notice_id)
    if notice.is_published:
        notice.view_count += 1
        db.session.commit()
        return render_template('notice_detail.html', notice=notice)
    else:
        flash('해당 공지사항을 찾을 수 없습니다.', 'error')
        return redirect(url_for('notices'))

# API Endpoints
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
    """Vercel 테스트 엔드포인트"""
    return jsonify({
        'message': 'BLH Company API is working!',
        'timestamp': datetime.utcnow().isoformat()
    })

@app.route('/api/inquiry', methods=['POST'])
def api_inquiry():
    """문의하기 API"""
    try:
        data = request.get_json()
        
        # 필수 필드 검증
        required_fields = ['name', 'email', 'message']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} is required'}), 400
        
        # 문의 저장
        inquiry = Inquiry(
            name=data['name'],
            email=data['email'],
            phone=data.get('phone', ''),
            company=data.get('company', ''),
            service_interest=data.get('service_interest', ''),
            message=data['message'],
            is_public=bool(data.get('is_public', True))
        )
        
        db.session.add(inquiry)
        db.session.commit()
        
        return jsonify({
            'message': '문의가 성공적으로 전송되었습니다.',
            'inquiry_id': inquiry.id
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/company-info')
def api_company_info():
    """회사 정보 조회 API"""
    return jsonify({
        'company_name': '비엘에이치컴퍼니 주식회사',
        'english_name': 'BLH COMPANY',
        'ceo': '홍독경',
        'capital': '1억원',
        'established': '2025년',
        'address': '부산시 해운대 우동 1436 카이저빌 613호',
        'phone': '051-711-4929',
        'fax': '031-715-4929',
        'email': 'info@blhcompany.com',
        'business_hours': '평일 09:00-18:00, 토요일 09:00-13:00, 일요일 휴무'
    })

# Admin Routes
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    """관리자 로그인"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username == 'bhl' and password == 'bhl1004':
            session['admin_logged_in'] = True
            flash('관리자로 로그인되었습니다.', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('잘못된 사용자명 또는 비밀번호입니다.', 'error')
    
    return render_template('admin/login.html')

@app.route('/admin/logout')
def admin_logout():
    """관리자 로그아웃"""
    session.pop('admin_logged_in', None)
    flash('로그아웃되었습니다.', 'info')
    return redirect(url_for('admin_login'))

@app.route('/admin/dashboard')
def admin_dashboard():
    """관리자 대시보드"""
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    
    # 통계 정보
    total_notices = Notice.query.count()
    published_notices = Notice.query.filter_by(is_published=True).count()
    total_inquiries = Inquiry.query.count()
    unprocessed_inquiries = Inquiry.query.filter_by(is_processed=False).count()
    
    stats = {
        'total_notices': total_notices,
        'published_notices': published_notices,
        'total_inquiries': total_inquiries,
        'unprocessed_inquiries': unprocessed_inquiries
    }
    
    return render_template('admin/dashboard.html', stats=stats)

@app.route('/admin/notices')
def admin_notices():
    """공지사항 관리"""
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    
    notices_list = Notice.query.order_by(Notice.created_at.desc()).all()
    return render_template('admin/notices.html', notices=notices_list)

@app.route('/admin/inquiries')
def admin_inquiries():
    """문의사항 관리 목록"""
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    items = Inquiry.query.order_by(Inquiry.created_at.desc()).all()
    return render_template('admin/inquiries.html', inquiries=items)

@app.route('/admin/inquiries/<int:inq_id>', methods=['GET', 'POST'])
def admin_inquiry_detail(inq_id):
    """문의 상세 + 답변 작성"""
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    inquiry = Inquiry.query.get_or_404(inq_id)
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'answer':
            content = request.form.get('content', '').strip()
            if content:
                ans = InquiryAnswer(inquiry_id=inq_id, content=content, admin_name='관리자')
                inquiry.is_processed = True
                db.session.add(ans)
                db.session.commit()
                flash('답변이 등록되었습니다.', 'success')
        elif action == 'toggle_public':
            inquiry.is_public = not inquiry.is_public
            db.session.commit()
            flash('공개 여부가 변경되었습니다.', 'success')
        elif action == 'toggle_processed':
            inquiry.is_processed = not inquiry.is_processed
            db.session.commit()
            flash('처리 상태가 변경되었습니다.', 'success')
        return redirect(url_for('admin_inquiry_detail', inq_id=inq_id))
    answers = InquiryAnswer.query.filter_by(inquiry_id=inq_id).order_by(InquiryAnswer.created_at.asc()).all()
    return render_template('admin/inquiry_detail.html', inquiry=inquiry, answers=answers)

@app.route('/admin/notices/new', methods=['GET', 'POST'])
def admin_notice_new():
    """공지사항 작성"""
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        priority = int(request.form.get('priority', 0))
        is_published = 'is_published' in request.form
        
        # 이미지 업로드 처리
        image_url = None
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename != '' and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                # 고유한 파일명 생성
                timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S_')
                filename = timestamp + filename
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(os.path.join(app.root_path, file_path))
                image_url = f'uploads/{filename}'
        
        notice = Notice(
            title=title,
            content=content,
            priority=priority,
            is_published=is_published,
            image_url=image_url
        )
        
        db.session.add(notice)
        db.session.commit()
        
        flash('공지사항이 성공적으로 작성되었습니다.', 'success')
        return redirect(url_for('admin_notices'))
    
    return render_template('admin/notice_form.html')

@app.route('/admin/notices/<int:notice_id>/edit', methods=['GET', 'POST'])
def admin_notice_edit(notice_id):
    """공지사항 수정"""
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    
    notice = Notice.query.get_or_404(notice_id)
    
    if request.method == 'POST':
        notice.title = request.form.get('title')
        notice.content = request.form.get('content')
        notice.priority = int(request.form.get('priority', 0))
        notice.is_published = 'is_published' in request.form
        notice.updated_at = datetime.utcnow()
        
        # 이미지 업로드 처리
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename != '' and allowed_file(file.filename):
                # 기존 이미지 파일 삭제
                if notice.image_url:
                    old_file_path = os.path.join(app.root_path, 'static', notice.image_url)
                    if os.path.exists(old_file_path):
                        os.remove(old_file_path)
                
                # 새 이미지 저장
                filename = secure_filename(file.filename)
                timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S_')
                filename = timestamp + filename
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(os.path.join(app.root_path, file_path))
                notice.image_url = f'uploads/{filename}'
        
        db.session.commit()
        
        flash('공지사항이 성공적으로 수정되었습니다.', 'success')
        return redirect(url_for('admin_notices'))
    
    return render_template('admin/notice_form.html', notice=notice)

@app.route('/admin/notices/<int:notice_id>/delete', methods=['POST'])
def admin_notice_delete(notice_id):
    """공지사항 삭제"""
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    
    notice = Notice.query.get_or_404(notice_id)
    db.session.delete(notice)
    db.session.commit()
    
    flash('공지사항이 성공적으로 삭제되었습니다.', 'success')
    return redirect(url_for('admin_notices'))

# Static Files
@app.route('/static/<path:filename>')
def static_files(filename):
    """정적 파일 서빙"""
    return app.send_static_file(filename)

@app.route('/sitemap.xml')
def sitemap():
    """사이트맵"""
    return app.send_static_file('sitemap.xml')

@app.route('/robots.txt')
def robots():
    """로봇 배제 표준"""
    return app.send_static_file('robots.txt')

# Error Handlers
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # Lightweight migration for existing SQLite
        with db.engine.connect() as conn:
            # Inquiry 테이블에 is_public 컬럼 추가
            cols = [r[1] for r in conn.exec_driver_sql("PRAGMA table_info(inquiry)").fetchall()]
            if 'is_public' not in cols:
                try:
                    conn.exec_driver_sql("ALTER TABLE inquiry ADD COLUMN is_public BOOLEAN DEFAULT 1")
                except Exception:
                    pass
            
            # Notice 테이블에 image_url 컬럼 추가
            notice_cols = [r[1] for r in conn.exec_driver_sql("PRAGMA table_info(notice)").fetchall()]
            if 'image_url' not in notice_cols:
                try:
                    conn.exec_driver_sql("ALTER TABLE notice ADD COLUMN image_url VARCHAR(500)")
                except Exception:
                    pass
        
        # 샘플 공지사항 생성
        if Notice.query.count() == 0:
            sample_notices = [
                Notice(
                    title="BLH COMPANY 홈페이지 오픈",
                    content="BLH COMPANY 공식 홈페이지가 오픈되었습니다. 다양한 서비스와 정보를 확인해보세요.",
                    priority=1,
                    is_published=True
                ),
                Notice(
                    title="EV 진단 솔루션 출시 예정",
                    content="전기차 배터리 상태를 실시간으로 측정하는 EV 진단 솔루션이 곧 출시됩니다.",
                    priority=0,
                    is_published=True
                ),
                Notice(
                    title="온라인 경매 플랫폼 베타 테스트",
                    content="C2B 온라인 중고차 경매 플랫폼의 베타 테스트를 진행합니다.",
                    priority=0,
                    is_published=True
                )
            ]
            
            for notice in sample_notices:
                db.session.add(notice)
            
            db.session.commit()
    
    app.run(debug=True, host='0.0.0.0', port=3001)
