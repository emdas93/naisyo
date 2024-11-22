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
        Schema::create('chat_rooms', function (Blueprint $table) {
            $table->id(); // Primary Key, Auto Increment
            $table->string('title'); // 방 이름
            $table->unsignedBigInteger('user_id')->nullable(); // 방 주인 (NULL 허용)
            $table->timestamps(); // created_at, updated_at

            // Foreign Key 설정
            // $table->foreign('user_id')->references('id')->on('users')->onDelete('cascade');
        });
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::dropIfExists('chat_rooms');
    }
};
