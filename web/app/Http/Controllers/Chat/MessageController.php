<?php

namespace App\Http\Controllers\Chat;

use App\Http\Controllers\Controller;
use Illuminate\Http\Request;
use App\Models\ChatMessage;

class MessageController extends Controller
{
  public function sendMessage(Request $request)
  {
    // 1. 입력값 검증
    $validatedData = $request->validate([
      'user_id' => 'required', // 유효한 사용자 ID인지 확인
      'room_id' => 'required', // 유효한 채팅방 ID인지 확인
      'message' => 'required|string|max:1000', // 메시지 내용 제한
    ]);

    // 2. 데이터 저장
    $message = ChatMessage::create([
      'user_id' => $validatedData['user_id'],
      'room_id' => $validatedData['room_id'],
      'message' => $request->message,
    ]);

    // 3. 응답 반환
    return response()->json([
      'status' => 'success',
      // 'message' => 'Message sent successfully!',
      'message' => $message,
      'data' => $message,
    ], 201); // HTTP 201 Created
  }

  public function getMessages(Request $request)
  {
    // 1. 입력값 검증
    $validatedData = $request->validate([
      'user_id' => 'required|integer|exists:users,id', // 유효한 사용자 ID인지 확인
      'room_id' => 'required|integer|exists:chat_rooms,id', // 유효한 채팅방 ID인지 확인
    ]);

    try {
      // 2. 메시지 조회
      $messages = ChatMessage::where('room_id', $validatedData['room_id'])
        ->orderBy('created_at', 'asc') // 메시지 생성 날짜순으로 정렬
        ->get();

      // 3. 응답 반환
      return response()->json([
        'status' => 'success',
        'room_id' => $validatedData['room_id'],
        'messages' => $messages,
      ], 200); // HTTP 200 OK
    } catch (\Exception $e) {
      // 에러 처리
      return response()->json([
        'status' => 'error',
        'message' => '메시지를 가져오는 중 오류가 발생했습니다.',
        'error' => $e->getMessage(),
      ], 500); // HTTP 500 Internal Server Error
    }
  }
}
