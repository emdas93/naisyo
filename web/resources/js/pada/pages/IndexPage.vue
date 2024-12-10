<template>
  <div class="flex flex-col lg:h-full">
    <AppHeader />

    <div class="flex lg:flex-row flex-1 mt-10">
      <!-- 왼쪽 메뉴 -->
      <div class="flex flex-col items-center py-7 bg-blue-800 w-7 h-20 rounded-s-md ms-3 text-white">
        <span class="-rotate-90 font-bold text-sm tracking-widest">MENU</span>
      </div>
      <div
        class="lg:w-1/6 w-full mb-16 bg-gray-100 shadow-lg p-4 flex flex-col overflow-y-scroll scrollbar-hide border-2 border-blue-700 rounded-sm">
        <h2 class="text-lg font-bold mb-4">채널</h2>
        <ul class="space-y-2 mb-5">
          <li v-for="(channel, index) in channels" :key="index" @click="selectChannel(index)"
            class="text-sm cursor-pointer p-2 rounded-lg hover:bg-blue-200"
            :class="{ 'bg-blue-100': selectedChannel === index }">
            {{ channel.title }}
          </li>
        </ul>
        <h2 class="text-lg font-bold mb-4">대화</h2>
        <div class="flex flex-col overflow-y-auto h-[500px] scrollbar-hide">
          <ul class="space-y-2">
            <li v-for="(room, index) in rooms" :key="index" @click="selectRoom(room.id)"
              class="text-sm cursor-pointer p-2 rounded-lg hover:bg-gray-200"
              :class="{ 'bg-blue-100': selectedRoom === room.id }">
              {{ room.title }}
            </li>
          </ul>
        </div>
      </div>

      <!-- 중앙 컨텐츠 -->
      <div
        class="lg:w-5/6 w-full bg-white flex flex-col items-center justify-end relative bg-center bg-no-repeat ps-4">
        <div class="absolute inset-0 flex items-center justify-center -z-10">
          <img src="../assets/images/posco.png" alt="POSCO" class="opacity-10">
        </div>
        <!-- 채팅 메시지 영역 -->
        <div ref="chatContainer"
          class="flex-grow w-3/4 rounded-sm p-4 overflow-y-scroll space-y-4 bg-gray-50 border-2 border-blue-700 h-64 scrollbar-hide"
          @scroll="handleScroll">
          <div v-for="(msg, index) in chatMessages" :key="index" class="flex"
            :class="{ 'justify-end': msg.user_id > 0, 'justify-start': msg.user_id == 0 }">
            <div :class="{
              'bg-blue-500 text-white text-sm': msg.user_id > 0,
              'bg-gray-200 text-black text-sm markdown-body': msg.user_id == 0
            }" class="px-4 py-2 rounded-lg max-w-full">
              <div v-html="msg.message"></div>
            </div>
          </div>
        </div>

        <!-- 입력 영역 -->
        <div class="w-full md:w-3/4 bg-white flex flex-col sm:flex-row mt-4 pt-4 mb-16">
          <textarea v-model="message" @keypress="handleKeydown" placeholder="메시지를 입력하세요"
            class="border rounded-lg p-3 flex-grow resize-none h-16"></textarea>
          <button @click="sendMessage"
            class="bg-blue-500 text-white font-semibold rounded-lg shadow-md sm:ml-2 mt-2 sm:mt-0 px-6 py-3 w-full sm:w-auto hover:bg-blue-600">
            전송
          </button>
        </div>
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
import AppHeader from "../components/AppHeader.vue";

export default {
  name: "IndexPage",
  components: { AppHeader },
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
    const md = markdownIt({
      html: true,
      highlight: function (str, lang) {
        if (lang && hljs.getLanguage(lang)) {
          try {
            return `<pre class="hljs"><code>${hljs.highlight(str, { language: lang }).value}</code></pre>`;
          } catch (__) { }
        }
        return `<pre class="hljs"><code>${md.utils.escapeHtml(str)}</code></pre>`;
      }
    })
      .use(markdownItAnchor, { slugify: (s) => uslug(s) })
      .use(markdownItTocDoneRight, {
        containerClass: 'toc',
        slugify: (s) => uslug(s),
        callback: (html, ast) => {
          toc.value = generateToc(ast);
          toc.value = `<nav>${toc.value}</nav>`;
        },
      })
    // .use(markdownItHighlightJS, { hljs });

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
      selectedRoom.value = 0;
      getRooms();
      chatMessages.splice(0);
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
      selectedChannel.value = channels.length;
    };

    const addNewRoom = (room_id, selectedChannel, title) => {
      rooms.splice(1, 0, {
        id: room_id,
        channel_id: selectedChannel,
        title: title,
      });
      selectedRoom.value = room_id;
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
          for (let i = 0; i < response.data.messages.length; ++i) {
            response.data.messages[i].message = md.render(response.data.messages[i].message);
          }
          chatMessages.splice(0, chatMessages.length, ...response.data.messages);
          scrollToBottom();
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
      };

      // 새로운 메시지에서 채팅을 보낼 경우 방 생성
      if (selectedRoom.value === 0) {
        try {
          const getTitleResponse = await fetch("http://localhost/api/chat/create-room", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
              user_id: authStore.user.id,
              channel_id: selectedChannel.value,
              message: newMessage.message,
            })
          });
          const data = await getTitleResponse.json();

          addNewRoom(data.room_id, selectedChannel.value, data.title);

        } catch (error) {
          console.error("방 생성 중 에러:", error);
        }
      }

      chatMessages.push(newMessage);
      scrollToBottom();
      const messageToSend = message.value;
      message.value = "";

      // 프롬프트 전송
      try {
        console.log(selectedRoom.value)
        const response = await fetch("http://localhost/api/chat/send-message", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            user_id: authStore.user.id,
            message: messageToSend,
            room_id: selectedRoom.value
          }),
        });

        let content = "";
        let tempContent = ""
        let chatIndex = chatMessages.push({ message: "", user_id: 0 }) - 1;

        const reader = response.body.getReader();
        const decoder = new TextDecoder("utf-8");

        while (true) {
          const { done, value } = await reader.read();
          if (done) {
            break;
          }

          content = decoder.decode(value, { stream: true });
          content = JSON.parse(content);
          tempContent += content[0].message;
          chatMessages.at(chatIndex).message = md.render(tempContent);
          scrollToBottom();
        }

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




<style>
@import '/node_modules/github-markdown-css/github-markdown-light.css';
@import '/node_modules/highlight.js/styles/github.css';

.markdown-body {
  min-height: auto !important;
  --tw-bg-opacity: 1;
  background-color: rgb(229 231 235 / var(--tw-bg-opacity, 1));
}



/* 기본적으로 스크롤바 숨김 */
.scrollbar-hide::-webkit-scrollbar {
  display: none;
}

.scrollbar-hide {
  scrollbar-width: none;
  /* Firefox */
}

.response {
  font-family: "Courier New", Courier, monospace;
  white-space: pre-wrap;
  overflow: hidden;
  /* 타이핑 효과를 위해 내용이 잘리도록 설정 */
  display: inline-block;
  /* 글자별 애니메이션 적용 가능 */
}

@keyframes typing {
  from {
    width: 0;
  }

  to {
    width: 100%;
  }
}

@keyframes blink-caret {

  from,
  to {
    border-right-color: transparent;
  }

  50% {
    border-right-color: black;
  }
}

.typing-effect {
  animation: typing 2s steps(30, end), blink-caret 0.5s step-end infinite;
  border-right: 2px solid black;
  white-space: nowrap;
  /* 텍스트를 한 줄로 유지 */
  overflow: hidden;
}
</style>
