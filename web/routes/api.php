<?php

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Route;

use App\Http\Controllers\Chat\RoomController;
use App\Http\Controllers\Chat\MessageController;

use App\Http\Controllers\Auth\LoginController;
use App\Http\Controllers\Auth\RegisterController;

Route::get('/csrf-token', function () {
    return response()->json(['csrfToken' => csrf_token()]);
});

// User Login
Route::post('/login', [LoginController::class, 'login']);
Route::post('/logout', [LoginController::class, 'logout'])->middleware('auth:sanctum');
Route::get('/user', [LoginController::class, 'user'])->middleware('auth:sanctum');

// Register
Route::post('/register', [RegisterController::class, 'register']);

// Message
Route::post('/message/send-message', [MessageController::class, 'sendMessage']);

// Room
Route::post('/chat/get-rooms', [RoomController::class, 'getRooms']);
Route::post('/chat/create-room', [RoomController::class, 'createRoom']);
Route::get('/chat/get-last-room-id', [RoomController::class, 'getLastRoomId']);
