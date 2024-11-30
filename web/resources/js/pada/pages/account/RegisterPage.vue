<template>
  <div class="flex flex-col justify-center items-center w-100 min-h-screen">
    <h3 class="font-bold text-3xl text-gray-500 mb-10">PADA REGISTER</h3>
    <form class="w-full max-w-lg" @submit.prevent="register">
      <div class="flex flex-wrap -mx-3 mb-6">
        <div class="w-full px-3 mb-6">
          <label class="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2" for="name">
            Full Name
          </label>
          <input
            v-model="name"
            class="appearance-none block w-full bg-gray-200 text-gray-700 border border-gray-200 rounded py-3 px-4 mb-3 leading-tight focus:outline-none focus:bg-white focus:border-gray-500"
            id="name"
            type="text"
            placeholder="John Doe"
          />
          <p v-if="errors.name" class="text-red-500 text-xs italic">{{ errors.name }}</p>
        </div>
      </div>
      <div class="flex flex-wrap -mx-3 mb-6">
        <div class="w-full px-3">
          <label class="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2" for="email">
            Email
          </label>
          <input
            v-model="email"
            class="appearance-none block w-full bg-gray-200 text-gray-700 border border-gray-200 rounded py-3 px-4 mb-3 leading-tight focus:outline-none focus:bg-white focus:border-gray-500"
            id="email"
            type="email"
            placeholder="you@example.com"
          />
          <p v-if="errors.email" class="text-red-500 text-xs italic">{{ errors.email }}</p>
        </div>
      </div>
      <div class="flex flex-wrap -mx-3 mb-6">
        <div class="w-full px-3">
          <label class="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2" for="password">
            Password
          </label>
          <input
            v-model="password"
            class="appearance-none block w-full bg-gray-200 text-gray-700 border border-gray-200 rounded py-3 px-4 mb-3 leading-tight focus:outline-none focus:bg-white focus:border-gray-500"
            id="password"
            type="password"
            placeholder="******************"
          />
          <p v-if="errors.password" class="text-red-500 text-xs italic">{{ errors.password }}</p>
        </div>
      </div>
      <div class="flex items-center justify-between">
        <button
          class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
          type="submit"
        >
          Register
        </button>
      </div>
    </form>
    <p class="text-center text-gray-500 text-xs mt-5">
      &copy;2024 Pada Team. All rights reserved.
    </p>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      name: "",
      email: "",
      password: "",
      errors: {},
    };
  },
  methods: {
    async register() {
      this.errors = {}; // Reset previous errors
      try {
        const response = await axios.post("http://localhost/api/register", {
          name: this.name,
          email: this.email,
          password: this.password,
        });

        alert("회원가입이 완료되었습니다!");
        console.log("Registration Response:", response.data);

        // 회원가입 후 로그인 페이지로 리다이렉트
        this.$router.push({ name: "login" });
      } catch (error) {
        if (error.response && error.response.data.errors) {
          this.errors = error.response.data.errors; // Laravel 유효성 검사 에러
        } else {
          console.error("Registration Error:", error);
        }
      }
    },
  },
};
</script>

<style>
html,
body {
  width: 100%;
  min-height: 100vh;
}
</style>
