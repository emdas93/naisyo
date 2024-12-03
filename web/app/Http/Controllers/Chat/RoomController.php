<?php

namespace App\Http\Controllers\Chat;

use App\Http\Controllers\Controller;
use Illuminate\Http\Request;
use App\Models\ChatRoom;

class RoomController extends Controller
{
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

  public function createRoom(Request $request)
  {
    // 요청 데이터 검증
    $validated = $request->validate([
      'user_id' => 'required|integer',
      'channel_id' => 'required|integer',
      'title' => 'required|string|max:255', // 방 이름 필드 추가
    ]);

    $userId = $validated['user_id'];
    $channelId = $validated['channel_id'];
    $title = $validated['title'];

    try {
      // 새로운 채팅방 생성
      $room = ChatRoom::create([
        'title' => $title,
        'user_id' => $userId,
        'channel_id' => $channelId,
      ]);

      // 유저를 방에 추가 (Many-to-Many 관계)
      // $room->users()->attach($userId);

      // 성공적으로 생성된 방 반환
      return response()->json([
        'success' => true,
        'message' => '채팅방이 성공적으로 생성되었습니다.',
        'room' => $room,
      ], 201);
    } catch (\Exception $e) {
      // 에러 처리
      return response()->json([
        'success' => false,
        'message' => '채팅방 생성 중 오류가 발생했습니다.',
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
