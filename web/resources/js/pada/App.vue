<template>
  <div class="min-h-screen flex">
    <!-- 왼쪽 채널 리스트 -->
    <div class="w-1/6 bg-white shadow-md p-4 flex flex-col">
      <h2 class="text-lg font-bold mb-4">Channels</h2>
      <ul class="space-y-2 flex-grow">
        <li class="text-red-500">● Everything</li>
        <li class="text-yellow-500">● Everything</li>
        <li class="text-green-500">● Everything</li>
        <li class="text-blue-500">● Everything</li>
        <li class="text-purple-500">● Everything</li>
        <li class="text-blue-500">● Everything</li>
        <li class="text-blue-500">● Everything</li>
      </ul>
    </div>

    <!-- 중앙 컨텐츠 -->
    <div
      class="w-4/6 bg-white shadow-md flex flex-col items-center justify-end relative bg-center bg-no-repeat bg-opacity-20">
      <div class="absolute inset-0 flex items-center justify-center -z-10">
        <img src="./assets/images/posco.png" alt="POSCO" class="opacity-20">
      </div>
      <div class="grid grid-cols-2 gap-4 w-3/4">
        <button class="border border-dashed border-blue-500 rounded-lg p-4 text-center text-sm">
          SD00001의 제강, 연주실적을 조회해줘
        </button>
        <button class="border border-dashed border-blue-500 rounded-lg p-4 text-center text-sm">
          SG00001의 전로 실적을 분석해줘
        </button>
        <button class="border border-dashed border-blue-500 rounded-lg p-4 text-center text-sm">
          SA53102 의 LF실적을 조회해줘
        </button>
        <button class="border border-dashed border-blue-500 rounded-lg p-4 text-center text-sm">
          CBA1234 코드를 분석해줘
        </button>
      </div>
      <div class="flex flex-row mt-8 mb-8 w-3/4">
        <input type="text" placeholder="무엇이든 물어보세요!" class="border rounded-lg p-2 w-full">
        <button
          class="bg-blue-500 text-white font-semibold rounded-lg shadow-md ms-2 px-6 py-3 w-20 hover:bg-blue-600 hover:shadow-lg active:bg-blue-700 transition duration-200">
          전송
        </button>


      </div>
    </div>

    <!-- 오른쪽 컨텐츠 -->
    <div class="w-1/6 bg-white shadow-md p-4 flex flex-col space-y-8">
      <div>
        <h2 class="text-lg font-bold mb-4">검색기간 변경</h2>
        <form class="space-y-2">
          <label class="flex items-center space-x-2">
            <input type="radio" name="period" value="7" class="text-blue-500">
            <span>7일</span>
          </label>
          <label class="flex items-center space-x-2">
            <input type="radio" name="period" value="15" class="text-blue-500">
            <span>15일</span>
          </label>
          <label class="flex items-center space-x-2">
            <input type="radio" name="period" value="30" class="text-blue-500" checked>
            <span>30일</span>
          </label>
          <label class="flex items-center space-x-2">
            <input type="radio" name="period" value="90" class="text-blue-500">
            <span>90일</span>
          </label>
          <label class="flex items-center space-x-2">
            <input type="radio" name="period" value="180" class="text-blue-500">
            <span>180일</span>
          </label>
        </form>
      </div>
      <div>
        <h2 class="text-lg font-bold mb-4">검색기간 변경</h2>
        <form class="space-y-2">
          <label class="flex items-center space-x-2">
            <input type="radio" name="period2" value="7" class="text-blue-500">
            <span>7일</span>
          </label>
          <label class="flex items-center space-x-2">
            <input type="radio" name="period2" value="15" class="text-blue-500">
            <span>15일</span>
          </label>
          <label class="flex items-center space-x-2">
            <input type="radio" name="period2" value="30" class="text-blue-500" checked>
            <span>30일</span>
          </label>
          <label class="flex items-center space-x-2">
            <input type="radio" name="period2" value="90" class="text-blue-500">
            <span>90일</span>
          </label>
          <label class="flex items-center space-x-2">
            <input type="radio" name="period2" value="180" class="text-blue-500">
            <span>180일</span>
          </label>
        </form>
      </div>
    </div>
  </div>
</template>
