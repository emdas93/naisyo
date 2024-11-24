from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # CORS 설정 추가

# 기본 경로('/')에 대한 엔드포인트
@app.route('/py/api/')
def home():
    return jsonify({
        "message": "Welcome to the Flask server!",
        "status": "success"
    })

# 테스트 데이터를 반환하는 엔드포인트
@app.route('/py/api/test', methods=['GET'])
def test():
    return jsonify({
        "id": 1,
        "name": "Test Data",
        "description": "This is a simple test response",
        "status": "active"
    })

if __name__ == '__main__':
    # 서버 실행 (5001번 포트)
    app.run(host='0.0.0.0', port=5001, debug=True)
