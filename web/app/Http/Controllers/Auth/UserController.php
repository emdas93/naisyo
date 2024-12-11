<?php

namespace App\Http\Controllers\Auth;

use App\Http\Controllers\Controller;
use Illuminate\Http\Request;

use Illuminate\Support\Facades\Auth;
use Illuminate\Support\Facades\Validator;
use App\Models\User;

class UserController extends Controller
{
    public function getUserInfo(Request $request)
    {
        return response()->json(auth()->user());
    }

    public function setInstructions(Request $request)
    {
        // 요청 데이터 검증
        $validator = Validator::make($request->all(), [
            'instructions' => 'string|max:5000', // instructions 필드 유효성 검사
        ]);

        if ($validator->fails()) {
            return response()->json([
                'status' => 'error',
                'message' => '검증 실패',
                'errors' => $validator->errors(),
            ], 422);
        }

        try {
            // 현재 인증된 사용자 가져오기
            $user = Auth::user();

            // instructions 업데이트
            $user->instructions = $request->input('instructions');
            $user->save();

            return response()->json([
                'status' => 'success',
                'message' => '인스트럭션이 저장되었습니다.',
            ]);
        } catch (\Exception $e) {
            // 예외 처리
            return response()->json([
                'status' => 'error',
                'message' => '인스트럭션 저장 중 오류가 발생했습니다.',
                'error' => $e->getMessage(),
            ], 500);
        }
    }

    public function getUserList(Request $request) {
        $user = User::get();

        return response()->json([
            'data'=> $user
        ]);
    }
}
