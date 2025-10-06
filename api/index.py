from flask import Flask, jsonify, render_template, request, redirect, url_for, session, flash
import os

# Vercel 환경에서 올바른 경로 설정
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
template_dir = os.path.join(parent_dir, 'templates')
static_dir = os.path.join(parent_dir, 'static')

# Flask 앱 생성 (템플릿과 정적 파일 경로 포함)
app = Flask(__name__, 
           template_folder=template_dir, 
           static_folder=static_dir)

# 세션 및 관리자 인증 설정 (환경변수 우선)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'blh-company-secret-key-2025')
ADMIN_USERNAME = os.getenv('ADMIN_USERNAME', 'admin')
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', 'blh_admin_2025!')

# 로그인 보호 데코레이터
from functools import wraps

def login_required(view_func):
    @wraps(view_func)
    def wrapper(*args, **kwargs):
        if not session.get('is_admin_authenticated'):
            # JSON 요청은 401 반환, 그 외는 로그인 페이지로 이동
            if request.is_json or request.headers.get('Accept') == 'application/json':
                return jsonify({ 'success': False, 'message': 'Authentication required' }), 401
            return redirect(url_for('admin_login'))
        return view_func(*args, **kwargs)
    return wrapper

@app.route('/')
def landing():
    """랜딩 페이지"""
    try:
        return render_template('landing.html')
    except Exception as e:
        return jsonify({
            'error': 'Template error',
            'message': str(e),
            'template_dir': template_dir
        }), 500

@app.route('/home')
def home():
    """홈페이지 (데이터베이스 없이)"""
    try:
        # 데이터베이스 없이 빈 리스트로 렌더링
        return render_template('home.html', latest_notices=[])
    except Exception as e:
        return jsonify({
            'error': 'Template error',
            'message': str(e),
            'route': '/home'
        }), 500

@app.route('/health')
def health():
    """헬스체크"""
    return jsonify({
        'status': 'healthy',
        'message': 'BLH Company API is working!'
    })

@app.route('/services')
def services():
    """서비스 소개"""
    try:
        return render_template('services.html')
    except Exception as e:
        return jsonify({
            'error': 'Template error',
            'message': str(e),
            'route': '/services'
        }), 500

@app.route('/about')
def about():
    """회사소개"""
    try:
        return render_template('about.html')
    except Exception as e:
        return jsonify({
            'error': 'Template error',
            'message': str(e),
            'route': '/about'
        }), 500

@app.route('/contact')
def contact():
    """문의하기"""
    try:
        return render_template('contact.html')
    except Exception as e:
        return jsonify({
            'error': 'Template error',
            'message': str(e),
            'route': '/contact'
        }), 500

# 공지 라우트 (더미 데이터)
from datetime import datetime

@app.route('/notices')
def notices():
    """공지사항 목록 (DB 없이 더미 데이터)"""
    try:
        dummy_notices = [
            {
                'id': 1,
                'title': '공지사항 예시 1',
                'content': '내용 예시',
                'author': '관리자',
                'created_at': datetime.utcnow(),
                'priority': 0,
                'is_published': True,
                'view_count': 0,
                'image_url': None,
            },
            {
                'id': 2,
                'title': '공지사항 예시 2',
                'content': '내용 예시',
                'author': '관리자',
                'created_at': datetime.utcnow(),
                'priority': 1,
                'is_published': True,
                'view_count': 0,
                'image_url': None,
            },
        ]
        return render_template('notices.html', notices=dummy_notices)
    except Exception as e:
        return jsonify({
            'error': 'Template error',
            'message': str(e),
            'route': '/notices'
        }), 500

@app.route('/notices/<int:notice_id>')
def notice_detail(notice_id: int):
    """공지사항 상세 (DB 없이 더미 데이터)"""
    try:
        dummy_notice = {
            'id': notice_id,
            'title': f'공지사항 예시 {notice_id}',
            'content': '상세 내용 예시',
            'author': '관리자',
            'created_at': datetime.utcnow(),
            'priority': 0,
            'is_published': True,
            'view_count': 0,
            'image_url': None,
        }
        return render_template('notice_detail.html', notice=dummy_notice)
    except Exception as e:
        return jsonify({
            'error': 'Template error',
            'message': str(e),
            'route': '/notices/<id>'
        }), 500

# 관리자 인증 라우트
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    """관리자 로그인"""
    try:
        if request.method == 'POST':
            # JSON 또는 Form 모두 지원
            if request.is_json:
                payload = request.get_json(silent=True) or {}
                username = payload.get('username', '')
                password = payload.get('password', '')
            else:
                username = request.form.get('username', '')
                password = request.form.get('password', '')

            if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
                session['is_admin_authenticated'] = True
                # JSON 요청은 JSON으로, 그 외는 대시보드로 리다이렉트
                if request.is_json:
                    return jsonify({'success': True, 'message': 'Login success'}), 200
                flash('로그인되었습니다.', 'success')
                return redirect(url_for('admin_dashboard'))
            else:
                if request.is_json:
                    return jsonify({'success': False, 'message': 'Invalid credentials'}), 401
                flash('아이디 또는 비밀번호가 올바르지 않습니다.', 'error')
                # 템플릿 없을 수도 있으므로 아래로 진행
        # GET 요청이거나 실패 시 템플릿 렌더링 시도
        return render_template('admin/login.html')
    except Exception as e:
        # 템플릿이 없거나 오류 발생시 JSON 플레이스홀더
        return jsonify({
            'page': 'admin_login',
            'message': 'Admin login placeholder',
            'error': str(e)
        })

@app.route('/admin/logout', methods=['POST', 'GET'])
@login_required
def admin_logout():
    session.pop('is_admin_authenticated', None)
    if request.is_json:
        return jsonify({'success': True, 'message': 'Logged out'}), 200
    return redirect(url_for('admin_login'))

@app.route('/admin')
@login_required
def admin_root():
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    try:
        stats = {
            'total_notices': 2,
            'published_notices': 2,
            'total_inquiries': 0,
            'unprocessed_inquiries': 0,
        }
        return render_template('admin/dashboard.html', stats=stats)
    except Exception:
        return jsonify({ 'page': 'admin_dashboard', 'status': 'ok' })

# 추가: 관리자 문의 목록 (더미)
@app.route('/admin/inquiries')
@login_required
def admin_inquiries():
    try:
        dummy_inquiries = []
        return render_template('admin/inquiries.html', inquiries=dummy_inquiries)
    except Exception as e:
        return jsonify({'page': 'admin_inquiries', 'inquiries': [], 'error': str(e)})

# 추가: 공지사항 작성 폼 (더미)
@app.route('/admin/notices/new')
@login_required
def admin_notice_new():
    try:
        return render_template('admin/notice_form.html', mode='create', notice=None)
    except Exception as e:
        return jsonify({'page': 'admin_notice_new', 'error': str(e)})

# 추가: 공지사항 관리 목록 (더미)
@app.route('/admin/notices')
@login_required
def admin_notices():
    try:
        dummy_notices = [
            {
                'id': 1,
                'title': '공지사항 예시 1',
                'author': '관리자',
                'created_at': datetime.utcnow(),
                'is_published': True,
                'priority': 0,
                'view_count': 0,
                'image_url': None,
            },
            {
                'id': 2,
                'title': '공지사항 예시 2',
                'author': '관리자',
                'created_at': datetime.utcnow(),
                'is_published': True,
                'priority': 1,
                'view_count': 5,
                'image_url': None,
            },
        ]
        return render_template('admin/notices.html', notices=dummy_notices)
    except Exception as e:
        return jsonify({'page': 'admin_notices', 'error': str(e)})

@app.route('/test')
def test():
    """테스트 라우트"""
    return jsonify({
        'test': 'success',
        'message': 'Test route is working!',
        'template_dir': template_dir,
        'static_dir': static_dir
    })

if __name__ == '__main__':
    app.run(debug=False)