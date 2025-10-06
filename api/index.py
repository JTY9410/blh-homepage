from flask import Flask, jsonify

# 매우 간단한 Flask 앱으로 시작
app = Flask(__name__)

@app.route('/')
def hello():
    """기본 라우트"""
    return jsonify({
        'message': 'BLH Company - Hello World!',
        'status': 'success',
        'version': '1.0.0'
    })

@app.route('/health')
def health():
    """헬스체크"""
    return jsonify({
        'status': 'healthy',
        'message': 'BLH Company API is working!'
    })

@app.route('/test')
def test():
    """테스트 라우트"""
    return jsonify({
        'test': 'success',
        'message': 'Test route is working!'
    })

if __name__ == '__main__':
    app.run(debug=False)