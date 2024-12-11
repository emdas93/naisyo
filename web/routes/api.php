<?php

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Route;

use App\Http\Controllers\Chat\RoomController;
use App\Http\Controllers\Chat\MessageController;

use App\Http\Controllers\Auth\LoginController;
use App\Http\Controllers\Auth\RegisterController;
use App\Http\Controllers\Auth\UserController;

Route::get('/csrf-token', function () {
    return response()->json(['csrfToken' => csrf_token()]);
});

// User Login
Route::post('/account/login', [LoginController::class, 'login']);
Route::post('/account/logout', [LoginController::class, 'logout'])->middleware('auth:sanctum');
Route::get('/account/get-user-info', [UserController::class, 'getUserInfo'])->middleware('auth:sanctum');
Route::get('/account/get-user-list', [UserController::class, 'getUserList'])->middleware('auth:sanctum');
Route::middleware('auth:sanctum')->post('/account/set-instructions', [UserController::class, 'setInstructions']);


// Register
Route::post('/register', [RegisterController::class, 'register']);

// Message
Route::post('/chat/send-message', [MessageController::class, 'sendMessage']);
Route::post('/chat/get-messages', [MessageController::class, 'getMessages']);

// Room
Route::post('/chat/get-rooms', [RoomController::class, 'getRooms']);
Route::post('/chat/create-room', [RoomController::class, 'createRoom']);
Route::get('/chat/get-last-room-id', [RoomController::class, 'getLastRoomId']);
