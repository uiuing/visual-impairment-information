<script>
import { computed, watch } from "vue";

import store from "../module";
import { init } from "../utils/c/audio";

const newsOK = computed(() => store.state.newsOK);
const isLoading = computed(() => store.state.isLoading);

const closeActive = () => {
  try {
    const tmpEl = document.getElementsByClassName("play-text")[0];
    const tmpName = tmpEl.className;
    tmpEl.className = tmpName.replace("play-text", "");
  } catch (er) {
    console.log(er);
  }
};
watch(newsOK, (newVal) => {
  if (newVal) {
    const parEl = document.getElementById("contentParent");
    parEl.addEventListener("click", (e) => {
      if (e.target.getAttribute("label-is-readable") && !isLoading.value) {
        let temPr = e.target.parentElement;
        let pr;
        while (true) {
          if (temPr.className === "wrapper") {
            pr = temPr;
            break;
          } else {
            temPr = temPr.parentElement;
          }
        }
        pr.scrollTo({
          top: e.target.offsetTop - window.screen.height / 4,
          behavior: "smooth",
        });
        if (store.state.playContent !== e.target.textContent) {
          try {
            document.getElementById("voiceAudio").pause();
            document.getElementById("voiceAudio").src = "/";
          } catch (er) {
            console.log(er);
          }
          store.commit("changeIsLoading", true);
          store.commit("changePlayContent", e.target.textContent);
          init(store.state.playContent, "新闻").then(() => {
            store.commit("changeIsLoading", false);
          });
          closeActive();
          e.target.className += " play-text";
        }
      }
    });
  }
});
</script>
<template>
  <audio id="voiceAudio" src="/" />
</template>
<style scoped>
audio {
  display: none;
}
</style>
