<script setup>
defineProps({
  currentRate: {
    type: Number,
    default: 0,
  },
});
</script>
<template>
  <div class="main">
    <div class="circle">
      <van-circle
        v-model:current-rate="currentRate"
        :rate="0"
        :speed="1"
        :text="
          currentRate === 0
            ? '稍等片刻'
            : currentRate >= 100
            ? '识别中 ...'
            : '请说话 ...'
        "
        stroke-width="150"
      />
    </div>
  </div>
</template>
<style scoped>
.main {
  position: fixed;
  top: 0;
  left: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 100%;
}

.van-circle {
  width: 150px !important;
  height: 150px !important;
}

.circle {
  display: flex;
  justify-content: center;
  width: 150px;
  height: 150px;
  padding: 10px;
  background-color: #fff;
  border-radius: 20px;
  box-shadow: 0 0 0 20px rgb(0 0 0 / 12%);
}
</style>
