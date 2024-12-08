<template>
  <div class="flex flex-col lg:h-full">
    <AppHeader />
    <div class="flex lg:flex-row flex-1">
      <!-- 왼쪽 메뉴 -->
      <div
        class="lg:w-1/6 w-full bg-gray-100 shadow-lg p-4 flex flex-col overflow-y-scroll border border-gray-200 rounded-lg">
        <h2 class="text-lg font-bold mb-4">유저 정보</h2>
        <ul class="space-y-2 mb-5">
          <li class="text-sm cursor-pointer p-2 rounded-lg hover:bg-blue-200 bg-blue-100">
            유저 프로필
          </li>
          <li class="text-sm cursor-pointer p-2 rounded-lg hover:bg-blue-200">
            활동 내역
          </li>
          <li class="text-sm cursor-pointer p-2 rounded-lg hover:bg-blue-200">
            설정
          </li>
        </ul>
      </div>

      <!-- 중앙 컨텐츠 -->
      <div
        class="lg:w-5/6 w-full bg-white shadow-md flex flex-col items-center justify-start relative bg-center bg-no-repeat ps-4">
        <div class="absolute inset-0 flex items-center justify-center -z-10">
          <img src="../../assets/images/posco.png" alt="POSCO" class="opacity-10">
        </div>

        <!-- 유저 상세 정보 -->
        <div class="w-5/6 bg-gray-50 border border-gray-200 rounded-lg p-6">
          <h2 class="text-2xl font-bold text-gray-700 mb-4">유저 상세 정보</h2>
          <div class="space-y-4">
            <div class="flex items-center">
              <div
                class="w-16 h-16 bg-blue-500 text-white rounded-full flex items-center justify-center text-3xl font-semibold">
                {{ user.name.charAt(0) }}
              </div>
              <div class="ml-4">
                <h3 class="text-lg font-semibold">{{ user.name }}</h3>
                <p class="text-gray-500 text-sm">{{ user.email }}</p>
              </div>
            </div>
            <div class="text-gray-600 text-sm">
              <p><span class="font-semibold">직원 번호:</span> {{ user.emp_no }}</p>
              <p>
                <span class="font-semibold">이메일 인증 날짜:</span>
                {{ user.email_verified_at ? user.email_verified_at : "인증되지 않음" }}
              </p>
              <p><span class="font-semibold">생성일:</span> {{ user.created_at }}</p>
            </div>
          </div>
        </div>

        <!-- 인스트럭션 -->
        <div class="w-5/6 bg-gray-50 border border-gray-200 rounded-lg p-6 mt-6">
          <h2 class="text-2xl font-bold text-gray-700 mb-4">인스트럭션</h2>
          <div class="space-y-4">
            <textarea v-model="user.instructions" placeholder="여기에 인스트럭션을 입력하세요..."
              class="w-full h-24 p-3 border rounded-lg bg-white text-gray-700 focus:outline-none focus:ring-2 focus:ring-blue-500"></textarea>
            <button @click="saveInstructions"
              class="bg-blue-500 text-white font-semibold rounded-lg shadow-md px-6 py-3 w-full hover:bg-blue-600">
              저장
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from "vue";
import axios from "axios";
import AppHeader from "../../components/AppHeader.vue";

export default {
  name: "UserInfoPage",
  components: { AppHeader },
  setup() {
    const user = ref(null);
    const instructions = ref("");

    // 유저 데이터 가져오기
    const fetchUserData = async () => {
      try {
        const response = await axios.get("/api/account/get-user-info");
        user.value = response.data;
      } catch (error) {
        console.error("유저 데이터를 가져오는 데 실패했습니다:", error);
      }
    };

    // 인스트럭션 저장하기
    const saveInstructions = async () => {
      try {
        if(user.value.instructions == "") {
          user.value.instructions = "-";
        }
        const response = await axios.post("/api/account/set-instructions", { instructions: user.value.instructions });
        alert("인스트럭션이 저장되었습니다.");
      } catch (error) {
        console.error("인스트럭션 저장 실패:", error);
        alert("인스트럭션을 저장하는 중 문제가 발생했습니다.");
      }
    };

    // 초기 데이터 로드
    fetchUserData();

    return {
      user,
      instructions,
      saveInstructions,
    };
  },
};

</script>

<style></style>
