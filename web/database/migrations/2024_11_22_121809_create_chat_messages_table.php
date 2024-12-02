<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    /**
     * Run the migrations.
     */
    public function up(): void
    {
        Schema::create('chat_messages', function (Blueprint $table) {
            $table->id(); // Primary Key, Auto Increment
            $table->unsignedBigInteger('user_id')->nullable(); // 소유자 (NULL 허용)
            $table->unsignedBigInteger('room_id')->nullable(); // 채팅방 번호 (FK)
            $table->text('message'); // 메시지 내용
            $table->timestamps(); // created_at, updated_at

            // Foreign Key 설정
            // $table->foreign('user_id')->references('id')->on('users')->onDelete('set null');
            // $table->foreign('room_id')->references('id')->on('chat_rooms')->onDelete('cascade');
        });
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::dropIfExists('chat_messages');
    }
};
