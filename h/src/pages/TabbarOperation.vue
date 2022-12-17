<script setup>
import Recorder from "js-audio-recorder";
import { computed, ref, watch } from "vue";

import AssistantStatus from "../components/TabbarOperation/AssistantStatus.vue";
import store from "../module";
import { voiceToText } from "../utils/api/voice";
import { init } from "../utils/c/audio";

const newsOK = computed(() => store.state.newsOK);

const active = ref("none");
const isPlay = ref(false);
const isLoading = computed(() => store.state.isLoading);
const readAloudTip = ref("提示");
const isNewState = ref(true);

watch(isLoading, (newVal) => {
  if (newVal) {
    readAloudTip.value = "语音加载...";
  }
});
watch(newsOK, (newVal) => {
  if (newVal) {
    const voiceAudio = document.getElementById("voiceAudio");
    voiceAudio.addEventListener(
      "ended",
      () => {
        try {
          const tmpEl = document.getElementsByClassName("play-text")[0];
          const tmpName = tmpEl.className;
          tmpEl.className = tmpName.replace("play-text", "");
        } catch (er) {
          console.log(er);
        }
        readAloudTip.value = "提示";
        isPlay.value = false;
        voiceAudio.src = "/";
        store.commit("changePlayContent", "");
        isNewState.value = true;
      },
      false
    );
    voiceAudio.addEventListener(
      "play",
      () => {
        isNewState.value = false;
        readAloudTip.value = "停止";
        isPlay.value = true;
      },
      false
    );
    voiceAudio.addEventListener(
      "pause",
      () => {
        isNewState.value = false;
        readAloudTip.value = "继续";
        isPlay.value = false;
      },
      false
    );
  }
});

const controlAudio = () => {
  if (isNewState.value) {
    store.commit("changeIsLoading", true);
    init("点击新闻文字内容，我将会为您朗读。", "新闻").then(() => {
      store.commit("changeIsLoading", false);
    });
  } else if (!isLoading.value) {
    if (isPlay.value) {
      document.getElementById("voiceAudio").pause();
    } else {
      document.getElementById("voiceAudio").play();
    }
  }
};

const optionChange = (option) => {
  active.value = option;
  setTimeout(() => {
    active.value = "none";
  }, 100);
  return option;
};

const isRecording = ref(false);

let recorder = null;
const voiceTips = ref("语音助手");

function blobToDataURI(blob, callback) {
  const reader = new FileReader();
  reader.onload = (e) => {
    callback(e.target.result);
  };
  reader.readAsDataURL(blob);
}

const currentRate = ref(0);

const voiceRecorder = () => {
  if (recorder) {
    recorder.stop();
    const blob = recorder.getWAVBlob();
    blobToDataURI(blob, (dataURI) => {
      voiceToText(dataURI.replace("data:audio/wav;base64,", "")).then((res) => {
        if (res.status === "error") {
          const voiceAudio = document.getElementById("voiceAudio");
          voiceAudio.src = "/";
          voiceAudio.src = `data:audio/x-wav;base64,${res.voice}`;
          voiceAudio.play();
          voiceAudio.addEventListener(
            "ended",
            () => {
              isRecording.value = false;
            },
            false
          );
        } else if (res.c === "channel") {
          store.commit("changeNavItem", res.content);
          setTimeout(() => {
            isRecording.value = false;
          }, 500);
        }
        voiceTips.value = "语音助手";
        console.log(res);
      });
    });
    recorder.destroy().then(() => {
      recorder = null;
    });
  } else {
    Recorder.getPermission().then(() => {
      init("请告诉我您的问题", "助手").then(() => {
        isRecording.value = true;
        recorder = new Recorder();
        const voiceAudio = document.getElementById("voiceAudio");
        voiceAudio.addEventListener(
          "ended",
          () => {
            recorder.start().then(() => {});
            voiceTips.value = "请说话...";
            currentRate.value = 0;
            const interval = setInterval(() => {
              currentRate.value += 0.1;
              if (currentRate.value >= 100) {
                clearInterval(interval);
                voiceRecorder();
              }
            }, 10);
          },
          false
        );
      });
    });
  }
};

const openImage = () => {
  try {
    document.getElementById("open-image").querySelector("input").click();
  } catch (er) {
    console.log(er);
  }
};
</script>
<template>
  <van-tabbar v-model="active" :before-change="optionChange" :border="false">
    <van-tabbar-item name="replay" @click="controlAudio">
      <span>{{ readAloudTip }}</span>
      <template #icon="props">
        <van-loading v-if="isLoading" />
        <div v-else>
          <van-icon v-if="isPlay" name="pause-circle-o" />
          <van-icon v-else name="play-circle-o" />
        </div>
      </template>
    </van-tabbar-item>
    <van-tabbar-item icon="service-o" name="service" @click="voiceRecorder"
      >{{ voiceTips }}
    </van-tabbar-item>
    <assistant-status v-if="isRecording" :current-rate="currentRate" />
    <van-tabbar-item icon="scan" name="scan" @click="openImage"
      >扫描
    </van-tabbar-item>
  </van-tabbar>
</template>
