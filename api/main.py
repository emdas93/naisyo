import os
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("app_key")
app.config['CORS_HEADERS'] = "Content-Type"

# CORS 설정
ALLOWED_ORIGINS = ['http://localhost:5001', 'http://127.0.0.1:5001']
CORS(app, resources={r"/py/api/*": {"origins": ALLOWED_ORIGINS}}, supports_credentials=True)

@app.route('/py/api')
def home():
    return jsonify({
        "message": "Welcome to the Flask server!",
        "status": "success"
    })

@app.route('/py/api/test', methods=['GET'])
def test():
    return jsonify({
        "id": 1,
        "name": "Sample Data",
        "description": "This is test data for Flask API",
        "status": "active"
    })

@app.route('/py/api/send-message', methods=['GET'])
def sendMessage():
    return jsonify({
        "message": "TEST"
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
