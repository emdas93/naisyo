<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class Message extends Model
{
    use HasFactory;

    protected $table = 'messages'; // 테이블 이름 설정

    // 대량 할당 가능한 필드 정의
    protected $fillable = [
        'user_id',   // 사용자 ID
        'room_id',   // 채팅방 ID
        'message',   // 메시지 내용
    ];
}
