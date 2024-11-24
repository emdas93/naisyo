import { defineConfig } from 'vite';
import laravel from 'laravel-vite-plugin';
import vue from '@vitejs/plugin-vue';

export default defineConfig({
    plugins: [
        laravel({
            input: ['resources/css/app.css',
                    'resources/js/app.js',
                    'resources/css/pada/style.css',
                    'resources/js/pada/main.js'
                ],
            refresh: true,
        }),
        vue()
    ],
    server: {
        https: false,   // HTTPS 비활성화
        host: true,     // 요청 수신 IP 설정
        port: 3000,
        hmr: {host: 'localhost', protocol: 'ws', port: 3000},   // HMR 엔더포인트 및 프로토콜 설정
    },
});
