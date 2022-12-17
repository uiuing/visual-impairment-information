<script setup>
import { ref } from "vue";

import store from "../../module";

defineProps({
  news: {
    type: Object,
    default: () => ({
      title: "",
      source: "",
      ptime: "",
      content: "",
      docid: "",
    }),
  },
});

let domReadList = [];
const playDomIndex = ref(1);

const randomStr = () => {
  const str = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXY";
  const len = Math.floor(Math.random() * 25) + 18;
  let result = "";
  for (let i = 0; i < len; i += 1) {
    result += str[Math.floor(Math.random() * str.length)];
  }
  return result;
};
const domParKey = ref(randomStr());
const playAll = () => {
  if (store.state.isPlayAllPageFlag !== domParKey.value) {
    store.commit("changeIsPlayAllPageFlag", domParKey.value);
  }
  domReadList = document
    .getElementsByClassName(domParKey.value)[0]
    .getElementsByClassName("label-is-readable");
  domReadList[0].click();
  const voiceAudio = document.getElementById("voiceAudio");
  voiceAudio.addEventListener(
    "ended",
    () => {
      if (
        store.state.isPlayAllPageFlag === domParKey.value &&
        playDomIndex.value !== 0
      ) {
        if (playDomIndex.value < domReadList.length) {
          domReadList[playDomIndex.value].click();
          playDomIndex.value += 1;
        } else {
          store.commit("changeIsPlayAll", false);
          playDomIndex.value = 0;
          domReadList = [];
        }
      } else {
        playDomIndex.value = 0;
      }
    },
    false
  );
};
</script>
<template>
  <div class="wrapper">
    <div :class="['main', domParKey]">
      <div class="title label-is-readable" label-is-readable="true">
        <span style="display: none">新闻标题；</span> {{ news.title }}
      </div>
      <div class="tips" @click="playAll"></div>
      <div
        v-if="news.src !== ''"
        class="source label-is-readable"
        label-is-readable="true"
      >
        <span style="display: none">内容来自；</span> {{ news.src }}
      </div>
      <div class="time label-is-readable" label-is-readable="true">
        {{ news.time }}
      </div>
      <div class="content" v-html="news['content']"></div>
    </div>
  </div>
</template>

<style scoped>
.wrapper {
  height: var(--auto-content-height);
  overflow-y: auto;
  scroll-behavior: smooth;
}

.main {
  padding: 15px;
  margin: 25px 25px 150px;
  border-radius: 15px;
  box-shadow: 0 0 12px rgb(0 0 0 / 12%);
}

.title {
  font-size: 17pt;
}

.source {
  margin-top: 10pt;
  font-size: var(--van-font-size-md);
  text-align: right;
}

.time {
  margin-bottom: 5pt;
  font-size: var(--van-font-size-md);
  color: var(--van-gray-7);
  text-align: right;
}

.content {
  margin-top: 15pt;
  font-size: var(--van-font-size-lg);
  line-height: var(--van-line-height-lg);
  word-break: break-all;
}

img {
  width: 100% !important;
}

.tips {
  position: relative;
  width: 120px;
  margin: 5px 0 15px -15px;
}

.tips::before {
  position: absolute;
  z-index: 1;
  height: 0;
  padding-right: 15px;
  font-weight: bold;
  line-height: 0px;
  color: #fff;
  content: "朗读全文";
  border: 15px solid #a20000;
  border-right-color: transparent;
  box-shadow: -9px 7px 12px 0 rgb(0 0 0 / 41%);
}

.tips::after {
  position: absolute;
  top: 30px;
  content: "";
  border: 4px solid #000;
  border-bottom-color: transparent;
  border-left-color: transparent;
}
</style>
