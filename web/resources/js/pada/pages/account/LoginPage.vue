<template>
    <AppHeader class="absolute w-full" />
    <div class="flex flex-col justify-center items-center w-100 min-h-screen">
        <img src="../../assets/images/logo.png" alt="" class="w-52 mb-3">
        <div class="flex flex-col w-full max-w-xs mb-40">
            <form class="flex flex-col bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4" @submit.prevent="submit">
                <div class="mb-4">
                    <label class="block text-gray-700 text-sm font-bold mb-2" for="email">
                        이메일
                    </label>
                    <input v-model="email"
                        class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                        id="email" type="email" placeholder="Email" />
                </div>
                <div class="mb-4">
                    <label class="block text-gray-700 text-sm font-bold mb-2" for="password">
                        비밀번호
                    </label>
                    <input v-model="password"
                        class="shadow appearance-none border  rounded w-full py-2 px-3 text-gray-700 mb-3 leading-tight focus:outline-none focus:shadow-outline"
                        id="password" type="password" placeholder="******************" />
                    <p v-if="errorMessage" class="text-red-500 text-xs italic">{{ errorMessage }}</p>
                </div>
                <div class="flex items-center justify-between">
                    <button
                        class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
                        type="submit">
                        로그인
                    </button>
                    <router-link class="inline-block align-baseline font-bold text-sm text-blue-500 hover:text-blue-800"
                        to="register">
                        회원가입
                    </router-link>
                    <a class="inline-block align-baseline font-bold text-sm text-blue-500 hover:text-blue-800" href="#">
                        비밀번호 찾기
                    </a>
                </div>
                <div class="flex flex-col mx-auto w-full h-full text-right justify-end">
                  <span class="text-[9px] mt-5 -mb-5">시스템 문의 : POSCO PADA팀 박현준 대리 (02-1234-1234)</span>
                </div>
            </form>
            <p class="text-center text-gray-500 text-xs">
                &copy; 2024 Pada Team. All rights reserved.
            </p>
        </div>
    </div>
</template>

<script>
import { ref } from "vue";
import { useAuthStore } from "../../store/auth";
import { useRouter } from "vue-router";
import AppHeader from "../../components/AppHeader.vue";

export default {
    name: "LoginPage",
    components: {
        AppHeader
    },
    setup() {
        const authStore = useAuthStore();
        const router = useRouter();

        const email = ref("");
        const password = ref("");
        const errorMessage = ref("");

        const submit = async () => {
            try {
                await authStore.login({ email: email.value, password: password.value });
                // alert("로그인 성공! 환영합니다.");

                // 이전 페이지로 리다이렉트
                const redirectPath = router.currentRoute.value.query.redirect || "/";
                router.push(redirectPath);
            } catch (error) {
                if (error.response?.status === 401) {
                    errorMessage.value = "이메일 또는 비밀번호가 올바르지 않습니다.";
                } else {
                    errorMessage.value = "로그인 중 오류가 발생했습니다. 다시 시도해주세요.";
                }
            }
        };

        return { email, password, errorMessage, submit };
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
