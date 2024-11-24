<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use App\Models\Channel;

class ChannelController extends Controller
{
    // 채널 데이터 가져오기
    public function getChannels()
    {
        try {
            $channels = Channel::all();
            return response()->json([
                'success' => true,
                'data' => $channels
            ]);
        } catch (\Exception $e) {
            \Log::error($e->getMessage());
            return response()->json([
                'success' => false,
                'message' => '서버 에러 발생'
            ], 500);
        }
    }

}
