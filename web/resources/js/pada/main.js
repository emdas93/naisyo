import axios from 'axios';
import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import { createPinia } from 'pinia';

axios.defaults.baseURL = 'http://localhost'; // API 서버 URL
axios.defaults.withCredentials = true; // 쿠키 포함 요청 활성화

const pinia = createPinia();
const app = createApp(App);

app.use(router)
    .use(pinia)
    .mount('#app');
