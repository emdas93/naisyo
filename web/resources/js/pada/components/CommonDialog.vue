<template>
  <dialog ref="dialog" class="rounded-lg shadow-lg bg-white p-6 w-96">
    <h3 class="text-lg font-semibold text-gray-800 mb-4">확인</h3>
    <p class="text-sm text-gray-600 mb-6">{{ message }}</p>
    <div class="flex justify-end space-x-4">
      <button
        @click="cancel"
        class="px-4 py-2 bg-gray-200 text-gray-800 rounded-lg hover:bg-gray-300"
      >
        취소
      </button>
      <button
        @click="confirm"
        class="px-4 py-2 bg-red-500 text-white rounded-lg hover:bg-red-600"
      >
        삭제
      </button>
    </div>
  </dialog>
</template>

<script>
import { ref } from "vue";

export default {
  props: {
    message: { type: String, default: "이 작업을 진행하시겠습니까?" },
  },
  emits: ["confirm"],
  setup(_, { emit }) {
    const dialog = ref(null);
    let param = null;

    const showModal = (data) => {
      param = data; // 유저 ID 저장
      dialog.value?.showModal();
    };

    const confirm = () => {
      emit("confirm", param); // 저장된 유저 ID를 emit
      dialog.value?.close();
    };

    const cancel = () => {
      dialog.value?.close();
    };

    return {
      dialog,
      showModal,
      confirm,
      cancel,
    };
  },
};
</script>
