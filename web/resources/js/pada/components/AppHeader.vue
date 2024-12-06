<template>
  <div>
    <!-- 공통 AppBar -->
    <div class="app-bar bg-blue-500 text-white shadow-md px-4 py-2 flex justify-between items-center">
      <div class="text-xl font-semibold">PADA(Posco Automated Data Analysis) 🤔</div>
      <div class="flex space-x-4">
        <router-link to="/" class="hover:bg-blue-600 rounded px-3 py-1 transition">홈</router-link>
        <router-link v-if="!isAuthenticated" to="/user/login"
          class="hover:bg-blue-600 rounded px-3 py-1 transition">로그인</router-link>
        <router-link v-if="!isAuthenticated" to="/user/register"
          class="hover:bg-blue-600 rounded px-3 py-1 transition">회원가입</router-link>
        <button v-if="isAuthenticated" @click="showLogoutModal"
          class="hover:bg-blue-600 rounded px-3 py-1 transition">로그아웃</button>
        <router-link v-if="isAuthenticated" to="/user/info"
          class="hover:bg-blue-600 rounded px-3 py-1 transition">유저정보</router-link>
      </div>
    </div>

    <div class="text-xl font-semibold">
      <img src="../assets/images/logo.png" class="m-5 w-40" alt="">
    </div>

    <!-- 로그아웃 확인 모달 -->
    <dialog ref="logoutDialog" class="rounded-lg shadow-lg p-4">
      <div class="text-center">
        <p class="text-lg font-semibold mb-4">정말 로그아웃하시겠습니까?</p>
        <div class="flex justify-center space-x-4">
          <button @click="confirmLogout" class="bg-red-500 text-white px-4 py-2 rounded hover:bg-red-600">예</button>
          <button @click="closeLogoutModal"
            class="bg-gray-300 text-gray-700 px-4 py-2 rounded hover:bg-gray-400">아니요</button>
        </div>
      </div>
    </dialog>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue';
import { useAuthStore } from '../store/auth';
import { useRouter } from 'vue-router';

export default {
  name: "AppHeader",
  setup() {
    const authStore = useAuthStore();
    const router = useRouter();
    const logoutDialog = ref(null); // dialog 참조

    // Pinia 상태와 직접 연동
    const isAuthenticated = computed(() => authStore.isAuthenticated);

    const showLogoutModal = () => {
      logoutDialog.value.showModal(); // dialog 열기
    };

    const closeLogoutModal = () => {
      logoutDialog.value.close(); // dialog 닫기
    };

    const confirmLogout = async () => {
      try {
        await authStore.logout(); // 로그아웃 요청 및 상태 초기화
        closeLogoutModal(); // dialog 닫기
        router.push({ name: 'login' }); // 로그인 페이지로 리다이렉트
      } catch (error) {
        console.error('Logout failed:', error.response?.data?.message || error.message);
      }
    };

    onMounted(() => {
      console.log("AppHeader");
    })

    return {
      isAuthenticated,
      logoutDialog,
      showLogoutModal,
      closeLogoutModal,
      confirmLogout,
    };
  },
}
</script>
