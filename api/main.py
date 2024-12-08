from flask import Flask, jsonify, request, Response, stream_with_context
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from datetime import datetime  # 현재 시간을 가져오기 위한 모듈
import tiktoken  # 토큰 계산용 라이브러리 (설치 필요)\
import json

from openai import OpenAI

app = Flask(__name__)

# MySQL 데이터베이스 설정
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://wxhack:qweQWE12!@localhost/wxhack'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 성능 최적화를 위해 비활성화

db = SQLAlchemy(app)

# CORS 설정
CORS(app, supports_credentials=True)

# 토큰 계산 함수
def calculate_tokens(messages, model="gpt-4o-mini"):
    encoding = tiktoken.encoding_for_model(model)
    total_tokens = 0
    for message in messages:
        total_tokens += len(encoding.encode(message['content']))
    return total_tokens

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

@app.route('/py/api/send-stream', methods=['POST'])
def sendStream():
    message = request.json['message']
    roomId = request.json['room_id']
    userId = request.json['user_id']

    # OpenAI 클라이언트 초기화
    client = OpenAI()
    
    # 기존 대화 기록 불러오기
    query = text("SELECT user_id, message FROM chat_messages WHERE room_id = :room_id ORDER BY created_at ASC LIMIT 20")
    past_messages = db.session.execute(query, {"room_id": roomId}).fetchall()

    # 유저 인스트럭션 불러오기
    instructionsQuery = text("SELECT instructions FROM users WHERE id=:user_id")
    user_instructions = db.session.execute(instructionsQuery, {"user_id": userId})
    
    # 대화 기록을 GPT 형식으로 변환
    messages = [{"role": "system", "content": "You are a helpful assistant."}]
    
    for instructions in user_instructions:
        messages.append({"role": "system", "content": instructions[0]})
        
    for past_message in past_messages:
        role = "user"
        if(past_message[0] == 0):
            role = "assistant"
        messages.append({"role": role, "content": past_message[1]})
    

        
    # 현재 사용자의 메시지 추가
    messages.append({"role": "user", "content": message})
    
    # 함수 정의
    functions = [
        {
            "name": "getUserInfo",
            "description": "Retrieve information about a specific user from the database.",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "integer",
                        "description": "The ID of the user whose information is being requested."
                    }
                },
                "required": ["user_id"]
            }
        },
        {
            "name": "sqlQueryBuilder",
            "description": "Build and execute SQL queries dynamically based on user input.",
            "parameters": {
                "type": "object",
                "properties": {
                    "prompt": {
                        "type": "string",
                        "description": "Natural language query describing the data to retrieve (e.g., 'Get all product names sold in Q3 2023')."
                    },
                },
                "required": ["prompt"]
            }
        }

    ]

    
    # print(messages)

    # 토큰 제한 처리
    max_tokens = 4000  # GPT 모델의 토큰 제한
    while calculate_tokens(messages) > max_tokens:
        # 오래된 메시지 제거
        messages.pop(1)  # 'system' 메시지는 유지하고, 가장 오래된 'user' 메시지를 제거

    # GPT 응답 생성
    # completion = client.chat.completions.create(
    #     model="gpt-4o-mini",
    #     messages=messages,
    #     functions=functions,
    #     stream=True
    # )

    # 스트리밍 응답을 처리하는 함수 정의
    def generate():
        full_response = ""
        
        completion = client.chat.completions.create(
            model="gpt-4",
            messages=messages,
            functions=functions,
            stream=True  # 스트리밍 활성화
        )

        for chunk in completion:
            print(chunk.choices[0])
            if chunk.choices[0].delta.function_call != None :
                if "functionName" not in locals() and chunk.choices[0].delta.function_call.name != None :
                    functionName = chunk.choices[0].delta.function_call.name
                    arguments_buffer = ""
                arguments_buffer += chunk.choices[0].delta.function_call.arguments
                print(arguments_buffer)
                
                
            if chunk.choices[0].finish_reason == "function_call":
                print("Function 수신 완료")
                print(functionName)
                
                try:
                    parsed_arguments = json.loads(arguments_buffer)
                    print(f"Parsed Arguments: {parsed_arguments}")  # 최종 파싱된 데이터 출력
                except json.JSONDecodeError as e:
                    print(f"JSON 파싱 오류: {e}")
                
                # 함수 이름이 `getUserInfo`인지 확인
                if functionName == "sqlQueryBuilder":
                    arguments = parsed_arguments
                    print(arguments)
                    
                    # OpenAI API에 새 요청 보내기
                    follow_up_response = client.chat.completions.create(
                        model="gpt-4",
                        messages=messages,  # 기존 메시지에 함수 결과 추가
                        stream=True  # 스트리밍 활성화
                    )

                    # 새 응답 스트리밍 처리
                    for follow_up_chunk in follow_up_response:
                        content = follow_up_chunk.choices[0].delta.content
                        if content:
                            full_response += content
                            yield content
                            
                    # 현재 시간 가져오기
                    now = datetime.utcnow()
                    # 새 메시지와 GPT 응답을 DB에 저장
                    insert_query = text(
                        "INSERT INTO chat_messages (user_id, room_id, message, created_at, updated_at) VALUES (:user_id, :room_id, :message, :created_at, :updated_at)"
                    )
                    db.session.execute(insert_query, {
                        "user_id": 0,
                        "room_id": roomId,
                        "message": full_response,
                        "created_at": now,
                        "updated_at": now
                    })  # GPT 응답은 user_id를 0으로 저장
                    db.session.commit()
                    
                # if functionName == "getUserInfo":
                #     # arguments에서 `user_id` 추출
                #     try:
                #         arguments = parsed_arguments
                #         requested_user_id = arguments.get("user_id")

                #         # 데이터베이스 쿼리 실행
                #         query = text("SELECT id, name, email, instructions, created_at FROM users WHERE id = :user_id")
                #         result = db.session.execute(query, {"user_id": requested_user_id}).fetchone()

                #         if result:
                #             user_data = {
                #                 "id": result.id,
                #                 "name": result.name,
                #                 "email": result.email,
                #                 "instructions": result.instructions,
                #                 "created_at": result.created_at.strftime("%Y-%m-%d %H:%M:%S")
                #             }
                #             # yield f"User Info: {user_data}\n"
                #             messages.append({
                #                 "role": "function",
                #                 "name": "getUserInfo",
                #                 "content": json.dumps(user_data)
                #             })
                #             # OpenAI API에 새 요청 보내기
                #             follow_up_response = client.chat.completions.create(
                #                 model="gpt-4",
                #                 messages=messages,  # 기존 메시지에 함수 결과 추가
                #                 stream=True  # 스트리밍 활성화
                #             )

                #             # 새 응답 스트리밍 처리
                #             for follow_up_chunk in follow_up_response:
                #                 content = follow_up_chunk.choices[0].delta.content
                #                 if content:
                #                     full_response += content
                #                     yield content
                                    
                #             # 현재 시간 가져오기
                #             now = datetime.utcnow()
                #             # 새 메시지와 GPT 응답을 DB에 저장
                #             insert_query = text(
                #                 "INSERT INTO chat_messages (user_id, room_id, message, created_at, updated_at) VALUES (:user_id, :room_id, :message, :created_at, :updated_at)"
                #             )
                #             db.session.execute(insert_query, {
                #                 "user_id": 0,
                #                 "room_id": roomId,
                #                 "message": full_response,
                #                 "created_at": now,
                #                 "updated_at": now
                #             })  # GPT 응답은 user_id를 0으로 저장
                #             db.session.commit()
                #         else:
                #             yield f"Error: User with ID {requested_user_id} not found.\n"
                #     except Exception as e:
                #         yield f"Error: Failed to process function call: {str(e)}\n"

            content = chunk.choices[0].delta.content
            if content:
                full_response += content
                yield content

        # 현재 시간 가져오기
        now = datetime.utcnow()

        # 새 메시지와 GPT 응답을 DB에 저장
        insert_query = text(
            "INSERT INTO chat_messages (user_id, room_id, message, created_at, updated_at) VALUES (:user_id, :room_id, :message, :created_at, :updated_at)"
        )
        db.session.execute(insert_query, {
            "user_id": 0,
            "room_id": roomId,
            "message": full_response,
            "created_at": now,
            "updated_at": now
        })  # GPT 응답은 user_id를 0으로 저장
        db.session.commit()
        
    return Response(stream_with_context(generate()))



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)


