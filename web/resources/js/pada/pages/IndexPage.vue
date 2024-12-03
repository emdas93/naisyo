<template>
  <div class="min-h-screen flex flex-col lg:flex-row">
    <!-- 왼쪽 채널 리스트 -->
    <div class="lg:w-1/6 w-full bg-white shadow-md p-4 flex flex-col order-1">
      <h2 class="text-lg font-bold mb-4">Channels</h2>
      <ul class="space-y-2 mb-5">
        <li v-for="(channel, index) in channels" :key="index" @click="selectChannel(index)"
          class="text-sm cursor-pointer p-2 rounded-lg hover:bg-gray-100"
          :class="{ 'bg-blue-100': selectedChannel === index }">
          {{ channel.title }}
        </li>
      </ul>
      <h2 class="text-lg font-bold mb-4">Rooms</h2>
      <ul class="space-y-2 mb-5">
        <li v-for="(room, index) in rooms" :key="index" @click="selectRoom(room.id)"
          class="text-sm cursor-pointer p-2 rounded-lg hover:bg-gray-100"
          :class="{ 'bg-blue-100': selectedRoom === room.id }">
          {{ room.title }}
        </li>
      </ul>
    </div>

    <!-- 중앙 컨텐츠 -->
    <div
      class="lg:w-5/6 w-full bg-white shadow-md flex flex-col items-center justify-end relative bg-center bg-no-repeat bg-opacity-20 p-4 order-3 lg:order-2">
      <div class="absolute inset-0 flex items-center justify-center -z-10">
        <img src="../assets/images/posco.png" alt="POSCO" class="opacity-20">
      </div>
      <!-- 채팅 메시지 영역 -->
      <div ref="chatContainer"
        class="flex-grow w-full md:w-full rounded-lg p-4 overflow-y-scroll space-y-2 h-64 scrollbar-hide"
        @scroll="handleScroll">
        <div v-for="(msg, index) in chatMessages" :key="index" class="flex"
          :class="{ 'justify-end': msg.user_id > 0, 'justify-start': msg.user_id == 0 }">
          <div :class="{
            'bg-blue-500 text-white': msg.user_id > 0,
            'text-black': msg.user_id == 0
          }" class="px-4 py-2 rounded-lg max-w-3xl text-wrap markdown-body" v-html="msg.message">
          </div>
        </div>
      </div>
      <!-- 입력 영역 -->
      <div class="w-full md:w-3/4 bg-white flex flex-col sm:flex-row mt-4 pt-4">
        <textarea v-model="message" @keydown="handleKeydown" placeholder="무엇이든 물어보세요!"
          class="border rounded-lg p-2 flex-grow resize-none h-16"></textarea>
        <button @click="sendMessage"
          class="bg-blue-500 text-white font-semibold rounded-lg shadow-md sm:ms-2 mt-2 sm:mt-0 px-6 py-3 w-full sm:w-auto hover:bg-blue-600 hover:shadow-lg active:bg-blue-700 transition duration-200">
          전송
        </button>
      </div>
    </div>

  </div>
</template>

<script>
import { ref, reactive, onMounted, nextTick } from "vue";
import markdownIt from 'markdown-it';
import markdownItAnchor from 'markdown-it-anchor';
import markdownItTocDoneRight from 'markdown-it-toc-done-right';
import markdownItHighlightJS from 'markdown-it-highlightjs';
import hljs from "highlight.js";
import matter from 'gray-matter';
import uslug from "uslug";
import axios from "axios";
import { useAuthStore } from "../store/auth";

export default {
  name: "IndexPage",
  setup() {
    // 데이터 정의
    const message = ref("");
    const chatMessages = reactive([]);
    const channels = reactive([]);
    const rooms = reactive([]);
    const selectedChannel = ref(0);
    const selectedRoom = ref(0);
    const startDate = ref("");
    const endDate = ref("");
    const chatContainer = ref(null);
    const toc = ref("");
    const authStore = useAuthStore();

    // Markdown 객체 정의
    const md = markdownIt({ html: true })
      .use(markdownItAnchor, { slugify: (s) => uslug(s) })
      .use(markdownItTocDoneRight, {
        containerClass: 'toc',
        slugify: (s) => uslug(s),
        callback: (html, ast) => {
          toc.value = generateToc(ast);
          toc.value = `<nav>${toc.value}</nav>`;
        },
      })
      .use(markdownItHighlightJS, { hljs });

    const generateToc = (node) => {
      let html = "";
      if (node.n) {
        const padding = node.l === 1 ? '' : 'ps-3';
        html += `<li class="text-sm text-slate-300 ${padding}"><a href="#${uslug(node.n)}">${node.n}`;
      }
      if (Array.isArray(node.c) && node.c.length > 0) {
        html += "<ul>";
        node.c.forEach(childNode => {
          html += generateToc(childNode);
        });
        html += "</ul>";
      }
      if (node.n) html += "</a></li>";
      return html;
    };

    // 메서드 정의
    const handleKeydown = (event) => {
      if (event.key === "Enter" && !event.shiftKey) {
        event.preventDefault();
        sendMessage();
      }
    };

    const selectChannel = (index) => {
      selectedChannel.value = index;
    };

    const selectRoom = (index) => {
      selectedRoom.value = index;
      if (selectedRoom.value !== 0) {
        getMessage();
      }
      else {
        chatMessages.splice(0)
      }
    };

    const addNewChannel = (title) => {
      channels.push({ title, messages: [] });
      selectedChannel.value = channels.length - 1;
    };

    const addNewRoom = (lastRoomId, selectedChannel, newMessage) => {
      rooms.splice(1, 0, {
        id: lastRoomId,
        channel_id: selectedChannel,
        title: newMessage,
      });
      selectedRoom.value = lastRoomId;
    };

    const getLastRoomId = async () => {
      try {
        const response = await axios.get("http://localhost/api/chat/get-last-room-id", {
          headers: { "Content-Type": "application/json" },
        });
        return response.data.success ? response.data.lastRoomId : 0;
      } catch (error) {
        console.error("API 요청 중 에러 발생:", error);
        return 0;
      }
    };

    const getMessage = async () => {
      try {
        const response = await axios.post(
          "http://localhost/api/chat/get-messages",
          { user_id: authStore.user.id, room_id: selectedRoom.value },
          { headers: { "Content-Type": "application/json" } }
        );
        if (response.data.status === "success") {
          chatMessages.splice(0, chatMessages.length, ...response.data.messages);
        } else {
          console.error("메시지 가져오기 실패:", response.data.message);
        }
      } catch (error) {
        console.error("메시지 가져오기 중 에러:", error);
      }
    };

    const sendMessage = async () => {
      if (!message.value.trim()) return;

      const newMessage = {
        message: message.value,
        user_id: authStore.user.id,
        isMine: true,
      };

      if (selectedRoom.value === 0) {
        const lastRoomId = await getLastRoomId();
        try {
          await axios.post(
            "http://localhost/api/chat/create-room",
            { user_id: authStore.user.id, channel_id: selectedChannel.value, title: newMessage.message },
            { headers: { "Content-Type": "application/json" } }
          );
          addNewRoom(lastRoomId + 1, selectedChannel.value, newMessage.message);
        } catch (error) {
          console.error("방 생성 중 에러:", error);
        }
      }

      chatMessages.push(newMessage);
      scrollToBottom();
      const messageToSend = message.value;
      message.value = "";

      try {
        await axios.post(
          "http://localhost/api/chat/send-message",
          { user_id: authStore.user.id, room_id: selectedRoom.value, message: messageToSend },
          { headers: { "Content-Type": "application/json" } }
        );
        scrollToBottom();
      } catch (error) {
        console.error("메시지 전송 중 에러:", error);
      }
    };

    const scrollToBottom = () => {
      nextTick(() => {
        if (chatContainer.value) {
          chatContainer.value.scrollTop = chatContainer.value.scrollHeight;
        }
      });
    };

    const getRooms = async () => {
      try {
        const response = await axios.post(
          "http://localhost/api/chat/get-rooms",
          { user_id: authStore.user.id, channel_id: selectedChannel.value },
          { headers: { "Content-Type": "application/json" } }
        );
        if (response.data.success) {
          rooms.splice(1, rooms.length, ...response.data.rooms);
        } else {
          console.error("방 리스트 가져오기 실패:", response.data.message);
        }
      } catch (error) {
        console.error("API 요청 중 에러 발생:", error);
      }
    };

    // 초기화
    onMounted(() => {
      channels.push({ id: 1, title: '광양제철소' });
      channels.push({ id: 2, title: '포항제철소' });
      rooms.push({ id: 0, title: '새로운 메시지' });
      getRooms();
    });

    return {
      message,
      chatMessages,
      startDate,
      endDate,
      chatContainer,
      handleKeydown,
      sendMessage,
      channels,
      rooms,
      selectChannel,
      selectedChannel,
      selectedRoom,
      addNewChannel,
      selectRoom,
      addNewRoom,
    };
  },
};
</script>




<style scoped>
@import '/node_modules/github-markdown-css/github-markdown-light.css';
@import '/node_modules/highlight.js/styles/vs.css';

.markdown-body {
  min-height: auto !important;
}

/* 스크롤바 숨기기 */
.scrollbar-hide::-webkit-scrollbar {
  display: none;
}

.scrollbar-hide {
  scrollbar-width: none;
  /* Firefox */
}
</style>
