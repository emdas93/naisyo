import { createRouter, createWebHistory, createMemoryHistory } from "vue-router/auto";
// import { routes } from 'vue-router/auto-routes'
// Components

// Index, Etc...
import IndexPage from "../pages/IndexPage.vue";
import DashboardPage from "../pages/DashboardPage.vue";

// Account
import LoginPage from "../pages/account/LoginPage.vue";
import RegisterPage from "../pages/account/RegisterPage.vue";

const routes = [
  // Index, Etc...
  { path: '/', name: 'index', component: IndexPage },
  { path: '/dashboard', name: 'dashboard', component: DashboardPage },

  // Account
  { path: '/login', name: 'login', component: LoginPage },
  { path: '/register', name: 'register', component: RegisterPage },
  
];

const isClient = typeof window !== 'undefined'

const router = createRouter({
  history: isClient
    ? createWebHistory(import.meta.env.BASE_URL)
    : createMemoryHistory(import.meta.env.BASE_URL),
  routes,
})

export default router