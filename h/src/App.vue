<script setup>
import localforage from "localforage";
import { onMounted, ref } from "vue";

import AudioPlugin from "./components/AudioPlugin.vue";
import Navigation from "./pages/NavigationCategory.vue";
import NewsContent from "./pages/NewsContent.vue";
import TabbarOperation from "./pages/TabbarOperation.vue";
import VoiceGuide from "./pages/VoiceGuide.vue";

const isOnceLoaded = ref(false);

document.addEventListener("keydown", (e) => {
  if (e.code === "End") {
    window.location.reload();
  }
});

onMounted(() => {
  document.body.style.setProperty(
    "--auto-content-height",
    `${
      window.screen.height -
      document.querySelector(
        "#app > div.van-tabbar.van-tabbar--fixed.van-safe-area-bottom"
      ).clientHeight -
      document.querySelector("#app > div.van-tabs.van-tabs--line").clientHeight
    }px`
  );
});

localforage.getItem("once-loaded").then((onceLoaded) => {
  if (!onceLoaded) {
    localforage.setItem("once-loaded", false);
    isOnceLoaded.value = true;
  }
});

window.addEventListener("contextmenu", function (e) {
  e.preventDefault();
});
</script>
<template>
  <navigation />
  <news-content />
  <tabbar-operation />
  <voice-guide v-if="isOnceLoaded" />
  <audio-plugin />
</template>
<style>
body {
  overflow: hidden;
}

.play-text {
  position: relative;
  padding: 10px;
  font-size: 18pt !important;
  line-height: 25pt !important;
  border-radius: 7px;
  box-shadow: 0 20px 48px 20px rgba(0, 0, 0, 0.2),
    0 12px 32px rgba(0, 0, 0, 0.21), 0 8px 20px -8px rgba(0, 0, 0, 0.23);
}

.van-tab {
  font-size: 25px !important;
}

.van-tabs--line .van-tabs__wrap {
  height: 60px !important;
}

.van-tabbar-item {
  font-size: 20px !important;
}

.van-tabbar {
  height: 58px;
}

* {
  -webkit-touch-callout: none;
  -webkit-user-select: none;
  -khtml-user-select: none;
  -moz-user-select: none;
  -ms-user-select: none;
  user-select: none;
}
</style>
