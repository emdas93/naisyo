<template>
    <div class="flex flex-col lg:h-full">
      <!-- 헤더 영역 -->
      <header class="bg-blue-500 text-white p-4 shadow-md">
        <h1 class="text-lg font-bold">대시보드</h1>
      </header>

      <!-- 본문 -->
      <div class="flex lg:flex-row flex-1">
        <!-- 왼쪽 메뉴 -->
        <div class="lg:w-1/6 w-full bg-gray-100 shadow-lg p-4 flex flex-col overflow-y-scroll border border-gray-200 rounded-lg">
          <h2 class="text-lg font-bold mb-4">채널</h2>
          <ul class="space-y-2 mb-5">
            <li
              v-for="(channel, index) in channels"
              :key="index"
              @click="selectChannel(index)"
              class="text-sm cursor-pointer p-2 rounded-lg hover:bg-blue-200"
              :class="{ 'bg-blue-100': selectedChannel === index }"
            >
              {{ channel.title }}
            </li>
          </ul>
          <h2 class="text-lg font-bold mb-4">대화</h2>
          <div class="flex flex-col overflow-y-auto h-[580px] scrollbar-hide">
            <ul class="space-y-2">
              <li
                v-for="(room, index) in rooms"
                :key="index"
                @click="selectRoom(room.id)"
                class="text-sm cursor-pointer p-2 rounded-lg hover:bg-gray-200"
                :class="{ 'bg-blue-100': selectedRoom === room.id }"
              >
                {{ room.title }}
              </li>
            </ul>
          </div>
        </div>

        <!-- 중앙 컨텐츠 -->
        <div class="lg:w-5/6 w-full bg-white shadow-md flex flex-col items-center justify-end relative ps-4">
          <!-- 배경 이미지 -->
          <div class="absolute inset-0 flex items-center justify-center -z-10">
            <img src="#" alt="Background" class="opacity-10">
          </div>

          <!-- 채팅 메시지 영역 -->
          <div
            ref="chatContainer"
            class="flex-grow w-full rounded-lg p-4 overflow-y-scroll space-y-4 bg-gray-50 border border-gray-200 h-64 scrollbar-hide"
          >
            <div
              v-for="(msg, index) in chatMessages"
              :key="index"
              class="flex"
              :class="{ 'justify-end': msg.user_id > 0, 'justify-start': msg.user_id == 0 }"
            >
              <div
                :class="{
                  'bg-blue-500 text-white text-sm': msg.user_id > 0,
                  'bg-gray-200 text-black text-sm': msg.user_id == 0
                }"
                class="px-4 py-2 rounded-lg max-w-full"
              >
                {{ msg.message }}
              </div>
            </div>
          </div>

          <!-- 입력 영역 -->
          <div class="w-full md:w-3/4 bg-white flex flex-col sm:flex-row mt-4 pt-4">
            <textarea
              v-model="message"
              placeholder="메시지를 입력하세요"
              class="border rounded-lg p-3 flex-grow resize-none h-16"
            ></textarea>
            <button
              @click="sendMessage"
              class="bg-blue-500 text-white font-semibold rounded-lg shadow-md sm:ml-2 mt-2 sm:mt-0 px-6 py-3 w-full sm:w-auto hover:bg-blue-600"
            >
              전송
            </button>
          </div>
        </div>
      </div>
    </div>
  </template>

  <script>
  export default {
    data() {
      return {
        channels: [
          { title: '일반 채널' },
          { title: '개발 채널' },
          { title: '디자인 채널' },
        ],
        rooms: [
          { id: 1, title: 'Room 1' },
          { id: 2, title: 'Room 2' },
          { id: 3, title: 'Room 3' },
        ],
        chatMessages: [
          { user_id: 0, message: '안녕하세요!' },
          { user_id: 1, message: '안녕하세요, 반갑습니다!' },
        ],
        selectedChannel: null,
        selectedRoom: null,
        message: '',
      };
    },
    methods: {
      selectChannel(index) {
        this.selectedChannel = index;
      },
      selectRoom(id) {
        this.selectedRoom = id;
      },
      sendMessage() {
        if (this.message.trim() === '') return;
        this.chatMessages.push({ user_id: 1, message: this.message });
        this.message = '';
      },
    },
  };
  </script>

  <style scoped>
  /* 추가적인 스타일을 여기 추가할 수 있습니다. */
  .scrollbar-hide::-webkit-scrollbar {
    display: none;
  }
  </style>
