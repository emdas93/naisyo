import axios from 'axios';
import { createRouter, createWebHistory, createMemoryHistory } from "vue-router/auto";
import { useAuthStore } from '../store/auth';

// Index, Etc...
import IndexPage from "../pages/IndexPage.vue";
import DashboardPage from "../pages/DashboardPage.vue";

// Account
import LoginPage from "../pages/account/LoginPage.vue";
import RegisterPage from "../pages/account/RegisterPage.vue";
import UserInfoPage from "../pages/account/UserInfoPage.vue";

const routes = [
  // Index, Etc...
  { path: '/', name: 'index', component: IndexPage, meta: { requiresAuth: true } },
  { path: '/dashboard', name: 'dashboard', component: DashboardPage, meta: { requiresAuth: true } },

  // Account
  { path: '/user/login', name: 'login', component: LoginPage, meta: { requiresGuest: true } },
  { path: '/user/register', name: 'register', component: RegisterPage, meta: { requiresGuest: true } },
  { path: '/user/info', name: 'info', component: UserInfoPage, meta: { requiresAuth: true } },
];

const isClient = typeof window !== 'undefined';

const router = createRouter({
  history: isClient
    ? createWebHistory(import.meta.env.BASE_URL)
    : createMemoryHistory(import.meta.env.BASE_URL),
  routes,
});

// 라우터 가드
router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore();

  // 인증이 필요한 페이지인지 확인
  if (to.matched.some(record => record.meta.requiresAuth)) {
    if (!authStore.user) {
      try {
        await authStore.fetchUser(); // 인증 상태 확인
        next(); // 인증 성공 시 진행
      } catch {
        next({ name: 'login', query: { redirect: to.fullPath } }); // 인증 실패 시 로그인 페이지로 리다이렉트
      }
    } else {
      next(); // 이미 로그인 상태라면 진행
    }
  }
  // 비로그인 사용자만 접근 가능한 페이지인지 확인
  else if (to.matched.some(record => record.meta.requiresGuest)) {
    if (authStore.user) {
      // 이전 라우터가 존재하면 이전 페이지로 리다이렉트, 없으면 홈 페이지로
      if (from.name) {
        next({ name: from.name }); // 이전 페이지로 리다이렉트
      } else {
        next({ name: 'index' }); // 홈 페이지로 리다이렉트
      }
    } else {
      next(); // 비로그인 상태라면 진행
    }
  } else {
    next(); // 인증이 필요 없는 페이지는 진행
  }
});


export default router;
