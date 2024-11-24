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
        "status": "active",
        "message": """
아래는 요청하신 쿼리문 입니다. (Flask)

```sql
SELECT no, name, room, room_id, heat, no, testcol, opsco, posco
FROM table_name AS Table
LEFT JOIN join_table_name AS JOIN_TABLE
ON TABLE.no = JOIN_TABLE.table_no
WHERE TABLE.id=1
```

query의 결과는 아래 표와 같습니다.

|no|name|room|room_id|heat|no|testcol|opsco|posco|
|---|---|---|---|---|---|---|---|---|
|데이터1|데이터2|데이터3|데이터1|데이터2|데이터3|데이터1|데이터2|데이터3|
|데이터4|데이터5|데이터6|데이터4|데이터5|데이터6|데이터4|데이터5|데이터6|
|데이터7|데이터8|데이터9|데이터7|데이터8|데이터9|데이터7|데이터8|데이터9|
|데이터1|데이터2|데이터3|데이터1|데이터2|데이터3|데이터1|데이터2|데이터3|
|데이터4|데이터5|데이터6|데이터4|데이터5|데이터6|데이터4|데이터5|데이터6|
|데이터7|데이터8|데이터9|데이터7|데이터8|데이터9|데이터7|데이터8|데이터9|
"""
    })

if __name__ == '__main__':
    # 서버 실행 (5001번 포트)
    app.run(host='0.0.0.0', port=5001, debug=True)
