<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use App\Models\Message;

class MessageController extends Controller
{
    public function sendMessage(Request $request) {
        // 1. 입력값 검증
        // $validatedData = $request->validate([
        //     'user_id' => 'required|exists:users,id', // 유효한 사용자 ID인지 확인
        //     'room_id' => 'required|exists:chat_rooms,id', // 유효한 채팅방 ID인지 확인
        //     'message' => 'required|string|max:1000', // 메시지 내용 제한
        // ]);

        // 2. 데이터 저장
        $message = Message::create([
            // 'user_id' => $validatedData['user_id'],
            // 'room_id' => $validatedData['room_id'],
            'message' => $request->message,
        ]);

        $message = <<<EOD
아래는 요청하신 쿼리문 입니다. (Laravel)

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
EOD;

        // 3. 응답 반환
        return response()->json([
            'status' => 'success',
            // 'message' => 'Message sent successfully!',
            'message' => $message,
            'data' => $message,
        ], 201); // HTTP 201 Created
    }
}
