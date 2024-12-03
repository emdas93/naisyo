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
          :class="{ 'justify-end': msg.isMine, 'justify-start': !msg.isMine }">
          <div :class="{
            'bg-blue-500 text-white': msg.isMine,
            'text-black': !msg.isMine
          }" class="px-4 py-2 rounded-lg max-w-3xl text-wrap markdown-body" v-html="msg.text">
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
    const channels = reactive([]);
    const rooms = reactive([]);
    const selectedChannel = ref(0); // 현재 선택된 채널
    const selectedRoom = ref(0); // 현재 선택된 채널
    const chatMessages = reactive([]);
    const startDate = ref(""); // 시작 날짜
    const endDate = ref("");   // 종료 날짜
    const chatContainer = ref(null);
    const toc = ref("");
    const authStore = useAuthStore();

    // Markdown 객체 정의
    const md = markdownIt({
      html: true,
    }).use(markdownItAnchor, { slugify: (s) => { return uslug(s) }, })
      .use(markdownItTocDoneRight, {
        containerClass: 'toc', // TOC 컨테이너 클래스 설정
        slugify: (s) => { return uslug(s) },
        callback: (html, ast) => {
          toc.value = generateToc(ast);
          toc.value = `<nav>${toc.value}</nav>`;
        }
      }).use(markdownItHighlightJS, {
        hljs: hljs
      });

    const generateToc = (node) => {
      let html = "";
      // 현재 노드의 이름이 있는 경우 li 요소로 감싸기
      if (node.n) {
        let padding = 'ps-3';
        if (node.l === 1) {
          padding = '';
        }
        html += `<li class="text-sm text-slate-300 ${padding}"><a href="#${uslug(node.n)}">${node.n}`;
      }

      // "c" 키가 배열이고, 배열에 요소가 있는 경우 ul로 감싸고 재귀 호출
      if (Array.isArray(node.c) && node.c.length > 0) {
        html += "<ul>";
        node.c.forEach(childNode => {
          html += generateToc(childNode); // 하위 노드를 재귀적으로 처리
        });
        html += "</ul>";
      }

      // 현재 노드가 li로 시작했다면 li를 닫기
      if (node.n) {
        html += "</a></li>";
      }

      return html;
    }

    // 메서드 정의
    const handleKeydown = (event) => {
      if (event.key === "Enter" && !event.shiftKey) {
        event.preventDefault();
        sendMessage();
      }
    };

    const selectChannel = (index) => {
      selectedChannel.value = index; // 선택된 채널 변경
    };

    const selectRoom = (index) => {
      console.log(index);
      selectedRoom.value = index; // 선택된 채널 변경
    };

    const addNewChannel = (title) => {
      channels.push({ title, messages: [] });
      selectedChannel.value = channels.length - 1; // 새로 추가된 채널로 이동
    };

    const addNewRoom = (title) => {
      rooms.push({ title, messages: [] });
      selectedRoom.value = rooms.length - 1; // 새로 추가된 채널로 이동
    };

    const getLastRoomId = async () => {
      try {
        // API 호출
        const response = await axios.get("http://localhost/api/chat/get-last-room-id", {
          headers: {
            "Content-Type": "application/json",
          },
        });

        // API 호출 성공 시 데이터 처리
        if (response.data.success) {
          console.log("마지막 방 번호:", response.data.lastRoomId);
          return response.data.lastRoomId; // 마지막 방 번호 반환
        } else {
          console.error("마지막 방 번호를 가져오는 데 실패했습니다:", response.data.message);
          return 0; // 실패 시 기본값 0 반환
        }
      } catch (error) {
        // 에러 처리
        console.error("API 요청 중 에러 발생:", error);
        return 0; // 실패 시 기본값 0 반환
      }
    };




    const sendMessage = async () => {

      if (message.value.trim() !== "") {
        const newMessage = { text: message.value, isMine: true };

        // 새로운 채팅일 경우 처리
        if (selectedRoom.value == 0) {
          console.log("Create New Room");

          const lastRoomId = await getLastRoomId();
          console.log(lastRoomId);

          try {
            const responseFromCreateRoom = await axios.post(
              "http://localhost/api/chat/create-room",
              {
                user_id: authStore.user.id,
                channel_id: selectedChannel.value,
                title: newMessage.text
              },
              {
                headers: { "Content-Type": "application/json" },
              }
            )
            console.log("방 만들기 요청 결과 : " + responseFromCreateRoom);
            rooms.splice(1, 0, {
              id: lastRoomId + 1,
              channel_id: selectedChannel.value,
              title: newMessage.text
            });
            // selectedRoom.value = roomNumber

          } catch (error) {
            console.log(error);
          }
        }

        // 로컬에 메시지 추가
        chatMessages.push(newMessage);

        // 스크롤 처리
        scrollToBottom();

        // 메시지 초기화
        const messageToSend = message.value;
        message.value = "";

        try {
          // Laravel 서버로 메시지 전송
          const responseFromLaravel = await axios.post(
            "http://localhost/api/message/send-message",
            {
              user_id: authStore.user.id,
              room_id: selectedRoom.value,
              message: messageToSend,
            },
            {
              headers: { "Content-Type": "application/json" },
            }
          );

          const responseDataFromLaravel = responseFromLaravel.data;
          console.log("Laravel 서버 응답:", responseDataFromLaravel);

          /******************************* FLASK ********************************/
          // const responseFromFlask = await axios.post(
          //   "http://localhost:5001/py/api/send-message",
          //   { message: messageToSend },
          //   {
          //     headers: {
          //       "Content-Type": "application/json",
          //     },
          //     withCredentials: true,
          //   }
          // );

          // const responseDataFromFlask = responseFromFlask.data;
          // console.log("Flask 서버 응답:", responseDataFromFlask);

          // chatMessages.push({
          //   text: md.render(responseDataFromFlask.message),
          //   isMine: false,
          // });
          /******************************* FLASK ********************************/

          // 스크롤 처리
          scrollToBottom();
        } catch (error) {
          console.error("메시지 전송 중 에러 발생:", error);
        }
      }
    };


    // 스크롤 아래로
    const scrollToBottom = () => {
      nextTick(() => {
        // if (chatContainer.value) {
        chatContainer.value.scrollTop = chatContainer.value.scrollHeight;
        // }
      });
    }

    // 초기화 및 라이프사이클 훅
    onMounted(() => {
      console.log("컴포넌트가 마운트되었습니다.");
      channels.push({ id: 1, title: '광양제철소', message: '' });
      channels.push({ id: 2, title: '포항제철소', message: '' });
      rooms.push({ id: 0, title: '새로운 메시지', message: '' });
      getRooms()
    });

    const getRooms = async () => {
      try {
        // API 요청
        const response = await axios.post(
          "http://localhost/api/chat/get-rooms",
          {
            user_id: authStore.user.id,
            channel_id: selectedChannel.value
          },
          {
            headers: {
              "Content-Type": "application/json",
            }
          }
        );

        if (response.data.success) {
          // 방 리스트 갱신
          rooms.splice(1, rooms.length, ...response.data.rooms);
        } else {
          console.error("방 리스트를 가져오는 데 실패했습니다:", response.data.message);
        }
      } catch (error) {
        console.error("API 요청 중 에러 발생:", error);
      }
    };


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
