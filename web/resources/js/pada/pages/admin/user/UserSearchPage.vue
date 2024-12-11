<template>
  <div
    class="lg:w-5/6 w-full bg-white shadow-md flex flex-col items-center justify-end relative bg-center bg-no-repeat ps-4">
    <!-- 유저 검색 영역 -->
    <div
      class="flex-grow w-full rounded-lg p-4 overflow-y-scroll space-y-4 bg-gray-50 border border-gray-200 h-64 scrollbar-hide">
      <div class="flex flex-row">
        <div class="inline-block relative w-auto me-3">
          <select
            class="block appearance-none w-full bg-white border border-gray-400 hover:border-gray-500 px-4 py-2 pr-8 rounded shadow leading-tight focus:outline-none focus:shadow-outline">
            <option value="0">검색 조건</option>
            <option value="1">유저 이름</option>
            <option value="2">유저 이메일</option>
          </select>
          <div class="pointer-events-none absolute inset-y-0 right-0 flex items-center px-2 text-gray-700">
            <svg class="fill-current h-4 w-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20">
              <path d="M9.293 12.95l.707.707L15.657 8l-1.414-1.414L10 10.828 5.757 6.586 4.343 8z" />
            </svg>
          </div>
        </div>
        <div class="me-3">
          <input
            class="shadow appearance-none border rounded w-64 py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
            id="username" type="text" placeholder="Username">
        </div>
        <div class="">
          <button
            class="bg-gray-500 hover:bg-gray-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline">
            <i class="bi bi-search"></i>
          </button>
        </div>
      </div>
      <div class="flex flex-row">
        <div class="w-full overflow-x-auto shadow-md sm:rounded-lg">
          <table class="w-full text-sm text-left text-gray-500 dark:text-gray-400">
            <thead class="text-xs text-gray-700 uppercase bg-gray-100">
              <tr>
                <th scope="col" class="px-6 py-3">
                  번호
                </th>
                <th scope="col" class="px-6 py-3">
                  이름
                </th>
                <th scope="col" class="px-6 py-3">
                  이메일
                </th>
                <th scope="col" class="px-6 py-3">
                  직번
                </th>
                <th scope="col" class="px-6 py-3">
                  권한
                </th>
                <th scope="col" class="px-6 py-3 text-center">
                  등록일자
                </th>
                <th scope="col" class="px-6 py-3 text-center">
                  액션
                </th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(user, index) in users" class="bg-white border-b hover:bg-gray-50">
                <td class="px-6 py-4 font-medium text-gray-900 whitespace-nowrap ">
                  {{ user.id }}
                </td>
                <td class="px-6 py-4">
                  {{ user.name }}
                </td>
                <td class="px-6 py-4">
                  {{ user.email }}
                </td>
                <td class="px-6 py-4">
                  {{ user.emp_no }}
                </td>
                <td class="px-6 py-4">
                  관리자
                </td>
                <td class="px-6 py-4 text-center">
                  {{ formatDate(user.created_at) }}
                </td>
                <td class="px-6 py-4 text-center">
                  <button class="text-blue-600 dark:text-blue-500 hover:underline">
                    수정
                  </button>
                  <button class="text-red-600 dark:text-red-500 hover:underline ml-2">
                    삭제
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, reactive, onMounted, nextTick } from "vue";
import { useAuthStore } from "../../../store/auth";

export default {
  name: "IndexPage",
  components: {},
  setup() {
    const users = reactive([]);

    const getUserList = async () => {
      const response = await fetch("http://localhost/api/account/get-user-list")
      const userList = await response.json()
      for (let index in userList.data) {
        users.push(userList.data[index]);
      }

    }

    const formatDate = (isoDate) => {
      const date = new Date(isoDate);
      const options = {
        year: "numeric",
        month: "2-digit",
        day: "2-digit",
        hour: "2-digit",
        minute: "2-digit",
        second: "2-digit",
        hour12: false, // 24시간 형식
      };
      return new Intl.DateTimeFormat("ko-KR", options).format(date);
    }

    onMounted(() => {
      getUserList();
    })
    return {
      users,
      getUserList,
      formatDate
    };
  },
};
</script>




<style>
@import '/node_modules/github-markdown-css/github-markdown-light.css';
@import '/node_modules/highlight.js/styles/github.css';
@import '/node_modules/bootstrap-icons/font/bootstrap-icons.min.css'
</style>
