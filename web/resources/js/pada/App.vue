<template>
    <!-- 페이지 컨텐츠 -->
    <RouterView />
</template>


<script>

import AppHeader from './components/AppHeader.vue';

export default {
    name: "App",
    setup() {

    }

};
</script>


<style>
/* 필요 시 스타일 추가 */
html, body, #app {
    width:100%;
    height:100%;
}

/* 기본적으로 스크롤바 숨김 */
*::-webkit-scrollbar {
  display: none;
}

* {
  scrollbar-width: none;
  /* Firefox */
}
</style>
