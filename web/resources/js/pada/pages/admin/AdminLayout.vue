<template>
    <div class="flex flex-col lg:h-full">
      <div class="flex flex-row">
        <div class="lg:w-1/6 w-full flex flex-col">
          <img src="../../assets/images/logo.png" class="m-5 w-40" alt="">
        </div>
      </div>
      <div class="flex lg:flex-row flex-1">
        <!-- 왼쪽 메뉴 -->
        <div
          class="lg:w-1/6 w-full bg-gray-100 shadow-lg p-4 flex flex-col overflow-y-scroll border border-gray-200 rounded-lg">
          <h2 class="text-lg font-bold mb-4">관리자 메뉴</h2>
          <ul class="space-y-2 mb-5">
            <li v-for="(menu, index) in menus" :key="index" @click="selectMenu(menu)"
              class="text-sm cursor-pointer p-2 rounded-lg hover:bg-blue-200"
              :class="{ 'bg-blue-100': selectedMenu === menu.id }">
              {{ menu.title }}
            </li>
          </ul>
        </div>

        <!-- 중앙 컨텐츠 -->
        <RouterView />
      </div>
    </div>
  </template>

  <script>
  import { ref, reactive, onMounted, nextTick } from "vue";
  import { useAuthStore } from "../../store/auth";
  import { useRouter } from "vue-router";

  export default {
    name: "AdminLayout",
    components: {},
    setup() {
      const menus = reactive([]);
      const selectedMenu = ref('');
      const users = reactive([]);

      const router = useRouter();

      const selectMenu = (menu) => {
        selectedMenu.value = menu.id;
        router.push(menu.url);

      }

      onMounted(() => {
        menus.push({ id: 1, url: '/admin/user/search', title: "유저 찾기" });
        menus.push({ id: 2, url: '/admin/user/register', title: "유저 등록" });
      })
      return {
        menus,
        selectedMenu,
        selectMenu,
      };
    },
  };
  </script>




  <style>
  @import '/node_modules/github-markdown-css/github-markdown-light.css';
  @import '/node_modules/highlight.js/styles/github.css';
  @import '/node_modules/bootstrap-icons/font/bootstrap-icons.min.css'
  </style>
