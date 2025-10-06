from flask import Flask, jsonify, render_template, request
import os
from datetime import datetime

# Vercel 환경에서 올바른 경로 설정
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
template_dir = os.path.join(parent_dir, 'templates')
static_dir = os.path.join(parent_dir, 'static')

# Flask 앱 생성 (템플릿과 정적 파일 경로 포함)
app = Flask(__name__, 
           template_folder=template_dir, 
           static_folder=static_dir)

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

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    """관리자 로그인 (템플릿 없을 경우에도 안전)"""
    try:
        if request.method == 'POST':
            return jsonify({'success': True, 'message': 'Login placeholder success'}), 200
        return render_template('admin/login.html')
    except Exception as e:
        return jsonify({
            'page': 'admin_login',
            'message': 'Placeholder admin login (template not found)',
            'error': str(e)
        })

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