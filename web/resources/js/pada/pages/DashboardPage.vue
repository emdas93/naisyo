<template>
  <div>
    <button @click="getUser">HELLO</button>
    <button @click="logout">로그아웃</button>
  </div>
</template>

<script>
import axios from 'axios';
import { useRouter } from 'vue-router';

export default {
  setup() {
    const router = useRouter(); // Vue Router 가져오기

    const getUser = async () => {
      try {
        // 유저 정보 가져오기
        const userResponse = await axios.get("/api/user", { withCredentials: true });
        console.log("User Info:", userResponse.data);
      } catch (error) {
        console.error("Failed to fetch user info:", error.response?.data || error.message);
      }
    };



    return {
      getUser,
      logout,
    };
  },
};
</script>

<style>
</style>
