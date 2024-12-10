<?php

namespace App\Http\Controllers\Chat;

use App\Http\Controllers\Controller;
use Illuminate\Http\Request;
use App\Models\ChatRoom;
use Illuminate\Support\Facades\Http;

class RoomController extends Controller
{
  public function createRoom(Request $request)
  {
    // 1. 입력값 검증
    $validatedData = $request->validate([
      'user_id' => 'required',
      'channel_id' => 'required',
      'message' => 'required|string|max:5000', // 메시지 내용 제한
    ]);

    $responseFromPython = Http::post("http://localhost:5001/py/api/generate-title", [
      'message' => $request->message,
    ]);

    // 2. 데이터 저장
    $message = ChatRoom::create([
      'user_id' => $validatedData['user_id'],
      'channel_id' => $validatedData['channel_id'],
      'title' => $responseFromPython->json()['response'],
    ]);

    return response()->json([
      'status' => 'success',
      'room_id' => $message->id,
      'title' => $responseFromPython->json()['response']
    ], 200);
  }

  public function getRooms(Request $request)
  {
    // 요청 데이터 검증
    $validated = $request->validate([
      'user_id' => 'required|integer',
      'channel_id' => 'required|integer',
    ]);

    $userId = $validated['user_id'];
    $channelId = $validated['channel_id'];

    try {
      // 해당 유저와 채널 ID에 해당하는 방 리스트 조회
      $rooms = ChatRoom::where('channel_id', $channelId)
        ->where('user_id', $userId)
        ->orderBy('id', 'desc')
        ->get();

      // 결과 반환
      return response()->json([
        'success' => true,
        'rooms' => $rooms,
      ], 200);
    } catch (\Exception $e) {
      // 에러 처리
      return response()->json([
        'success' => false,
        'message' => '채팅방 조회 중 오류가 발생했습니다.',
        'error' => $e->getMessage(),
      ], 500);
    }
  }

  public function getLastRoomId(Request $request)
  {
    try {
      // 마지막 방 번호 가져오기
      $lastRoomId = ChatRoom::max('id');

      return response()->json([
        'success' => true,
        'lastRoomId' => $lastRoomId ?? 0, // 방이 없을 경우 0 반환
      ], 200);
    } catch (\Exception $e) {
      return response()->json([
        'success' => false,
        'message' => '마지막 방 번호를 가져오는 중 오류가 발생했습니다.',
        'error' => $e->getMessage(),
      ], 500);
    }
  }
}
