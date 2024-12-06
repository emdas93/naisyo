from flask import Flask, jsonify, request, Response, stream_with_context
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from datetime import datetime  # 현재 시간을 가져오기 위한 모듈

from openai import OpenAI

app = Flask(__name__)

# MySQL 데이터베이스 설정
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://wxhack:qweQWE12!@localhost/wxhack'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 성능 최적화를 위해 비활성화

db = SQLAlchemy(app)

# CORS 설정
CORS(app, supports_credentials=True)

@app.route('/py/api/get-title', methods=['POST'])
def getTitle():
    client = OpenAI()

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "입력 받은 프롬프트를 요약해서 15자 이내로(되도록이면) 제목을 만들어줘"},
            {
                "role": "user",
                "content": request.json['message']
            }
        ]
    )
    
    response_message = completion.choices[0].message.content
    
    return jsonify({
        "response": response_message
    })

@app.route('/py/api/send-message', methods=['POST'])
def sendMessage():
    message = request.json['message']
    roomId = request.json['room_id']
    userId = 0  # 사용자의 ID (로그인 기능이 없을 경우 기본값 설정)

    # OpenAI 클라이언트 초기화
    client = OpenAI()

    # 기존 대화 기록 불러오기
    query = text("SELECT message FROM chat_messages WHERE room_id = :room_id ORDER BY created_at ASC")
    past_messages = db.session.execute(query, {"room_id": roomId}).fetchall()

    # 대화 기록을 GPT 형식으로 변환
    messages = [{"role": "system", "content": "You are a helpful assistant."}]
    for past_message in past_messages:
        messages.append({"role": "user", "content": past_message[0]})

    # 현재 사용자의 메시지 추가
    messages.append({"role": "user", "content": message})

    # GPT 응답 생성
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages
    )

    response_message = completion.choices[0].message.content

    # 현재 시간 가져오기
    now = datetime.utcnow()

    # 새 메시지와 GPT 응답을 DB에 저장
    insert_query = text(
        "INSERT INTO chat_messages (user_id, room_id, message, created_at, updated_at) VALUES (:user_id, :room_id, :message, :created_at, :updated_at)"
    )
    db.session.execute(insert_query, {
        "user_id": 0,
        "room_id": roomId,
        "message": response_message,
        "created_at": now,
        "updated_at": now
    })  # GPT 응답은 user_id를 0으로 저장
    db.session.commit()

    return jsonify({
        'response': response_message
    })

@app.route('/py/api/send-message-stream', methods=['POST'])
def sendMessageStream():

    message = request.json['message']
    roomId = request.json['room_id']
    
    # OpenAI 클라이언트 초기화
    client = OpenAI()

    # 기존 대화 기록 불러오기
    query = text("SELECT message FROM chat_messages WHERE room_id = :room_id ORDER BY created_at ASC")
    past_messages = db.session.execute(query, {"room_id": roomId}).fetchall()

    # 대화 기록을 GPT 형식으로 변환
    messages = [{"role": "system", "content": "You are a helpful assistant."}]
    for past_message in past_messages:
        messages.append({"role": "user", "content": past_message[0]})

    # 현재 사용자의 메시지 추가
    messages.append({"role": "user", "content": message})

    # 스트리밍 응답을 처리하는 함수 정의
    def generate():
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            stream=True  # 스트리밍 활성화
        )
        print("A")
        for chunk in completion:
            if 'choices' in chunk and chunk['choices']:
                content = chunk['choices'][0].get('delta', {}).get('content', '')
                print("B")
                if content:
                    yield content

    return Response(stream_with_context(generate()), content_type='text/event-stream')

@app.route('/py/api/send-stream', methods=['POST'])
def sendStream():
    message = request.json['message']
    roomId = request.json['room_id']
    userId = 0  # 사용자의 ID (로그인 기능이 없을 경우 기본값 설정)

    # OpenAI 클라이언트 초기화
    client = OpenAI()

    # 기존 대화 기록 불러오기
    query = text("SELECT message FROM chat_messages WHERE room_id = :room_id ORDER BY created_at ASC")
    past_messages = db.session.execute(query, {"room_id": roomId}).fetchall()

    # 대화 기록을 GPT 형식으로 변환
    messages = [{"role": "system", "content": "You are a helpful assistant."}]
    for past_message in past_messages:
        messages.append({"role": "user", "content": past_message[0]})

    # 현재 사용자의 메시지 추가
    messages.append({"role": "user", "content": message})

    # GPT 응답 생성
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        stream=True
    )

    # 스트리밍 응답을 처리하는 함수 정의
    def generate():
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            stream=True  # 스트리밍 활성화
        )
        for chunk in completion:
            content = chunk.choices[0].delta.content
            if content:
                yield content
            
        # for chunk in completion:
        #     if 'choices' in chunk and chunk['choices']:
        #         content = chunk['choices'][0].get('delta', {}).get('content', '')
        #         print("B")
        #         if content:
        #             yield content

    return Response(stream_with_context(generate()))

    response_message = completion.choices[0].message.content

    # 현재 시간 가져오기
    now = datetime.utcnow()

    # 새 메시지와 GPT 응답을 DB에 저장
    insert_query = text(
        "INSERT INTO chat_messages (user_id, room_id, message, created_at, updated_at) VALUES (:user_id, :room_id, :message, :created_at, :updated_at)"
    )
    db.session.execute(insert_query, {
        "user_id": 0,
        "room_id": roomId,
        "message": response_message,
        "created_at": now,
        "updated_at": now
    })  # GPT 응답은 user_id를 0으로 저장
    db.session.commit()

    return jsonify({
        'response': response_message
    })

@app.route('/stream', methods=['POST'])
def streamed_response():
    def generate():
        yield 'Hello '
        yield 'My Name is'
        yield 'chu '
        yield 'seung '
        yield 'hyeop '
        yield '!'
        yield '!'
    return Response(stream_with_context(generate()))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)


