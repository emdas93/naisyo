<template>
  <div>
    <button @click="getUser()">HELLO</button>
  </div>
</template>
<script>
import axios from 'axios';

export default {
  setup() {
    const getUser = async() => {
      // 유저 정보 가져오기
      const userResponse = await axios.get("/api/user");
      console.log("User Info:", userResponse.data);
    }

    return{
      getUser
    }
  },

  mounted() {

  }
}
</script>
<style></style>
