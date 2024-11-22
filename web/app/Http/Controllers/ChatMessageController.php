<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use App\Models\ChatMessage;

class ChatMessageController extends Controller
{
    public function sendMessage(Request $request) {
        // 1. 입력값 검증
        // $validatedData = $request->validate([
        //     'user_id' => 'required|exists:users,id', // 유효한 사용자 ID인지 확인
        //     'room_id' => 'required|exists:chat_rooms,id', // 유효한 채팅방 ID인지 확인
        //     'message' => 'required|string|max:1000', // 메시지 내용 제한
        // ]);

        // 2. 데이터 저장
        $chatMessage = ChatMessage::create([
            // 'user_id' => $validatedData['user_id'],
            // 'room_id' => $validatedData['room_id'],
            'message' => $request->message,
        ]);

        // 3. 응답 반환
        return response()->json([
            'status' => 'success',
            'message' => 'Message sent successfully!',
            'data' => $chatMessage,
        ], 201); // HTTP 201 Created
    }
}
