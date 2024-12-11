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

    public function searchUserList(Request $request)
    {
        // 요청 데이터 검증
        $validatedData = Validator::make($request->all(), [
            'searchType' => 'numeric',
            'searchText' => 'string',
        ]);

        $searchType = $request->searchType;
        $searchText = $request['searchText'];

        $user = new User();

        if ($searchType == 1) {
            $searchType = 'name';
        } else if ($searchType == 2) {
            $searchType = 'email';
        }
        $user = User::where($searchType, 'like', '%' . $searchText . '%')->get();

        return response()->json($user);
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

    public function getUserList(Request $request)
    {
        // 한 페이지에 표시할 데이터 개수 (기본값: 10)
        $perPage = $request->input('per_page', 10);

        // 페이지네이션 적용
        $users = User::paginate($perPage);

        return response()->json($users);
    }


    public function deleteUser(Request $request)
    {
        // 요청 데이터 검증
        $validatedData = Validator::make($request->all(), [
            'user_id' => 'require|numeric',
        ]);

        User::where('id', $request['user_id'])->delete();
    }

    public function deleteUsers(Request $request)
    {
        // 요청 데이터 검증
        $validatedData = Validator::make($request->all(), [
            'user_ids' => 'require',
        ]);

        User::where('id', $request['user_ids'])->delete();
    }
}
