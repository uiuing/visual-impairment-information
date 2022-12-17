<script setup>
import { Toast } from "vant";
import { computed, ref, watch } from "vue";
import { useStore } from "vuex";

import getCategoryNews from "../utils/api/news";
import { init } from "../utils/c/audio";

const store = useStore();
const newsData = computed(() => store.state.news.data);
const navItem = computed(() => store.state.navItem);
const isRe = ref(true);
const loading = ref(false);
let toast = null;
const isTop = ref(true);
const scanArray = computed(() => store.state.scanArray);

const changeData = async () => {
  const labels = document.getElementsByClassName("readable-par");
  for (let i = 0; i < labels.length; i += 1) {
    const s = labels[i].textContent;
    if (s.length >= 110) {
      labels[i].className = "readable-par";
      // eslint-disable-next-line prefer-regex-literals
      const ns = s.match(new RegExp(".{0,120}[,，。；]", "g"));
      // eslint-disable-next-line no-restricted-syntax
      for (const j in ns) {
        if (j === 0) {
          ns[j] = `${ns[j]}</p>`;
        } else if (j === ns.length - 1) {
          ns[
            j
          ] = `<p class="label-is-readable" label-is-readable="true">${ns[j]}`;
        } else {
          ns[
            j
          ] = `<p class="label-is-readable" label-is-readable="true">${ns[j]}</p>`;
        }
      }
      try {
        labels[i].innerHTML = ns.join("");
      } catch (er) {
        console.log(er);
      }
    }
  }
};

const toastLoading = () => {
  isRe.value = false;
  store.commit("changeNewsOK", false);
  toast = Toast.loading({
    message: "加载中...",
    forbidClick: true,
    loadingType: "spinner",
    duration: 0,
  });
};

const getNews = async (category) => {
  try {
    document.getElementById("voiceAudio").pause();
    document.getElementById("voiceAudio").src = "/";
  } catch (er) {
    console.log(er);
  }
  const res = await getCategoryNews(category, 5);
  for (let i = 0; i < res.length; i += 1) {
    store.commit("addNews", res[i]);
  }

  setTimeout(() => {
    document
      .getElementsByClassName("wrapper")[0]
      .addEventListener("scroll", (e) => {
        isTop.value = e.target.scrollTop === 0;
      });
    store.commit("changeNewsOK", true);
    changeData().then(() => {
      isRe.value = true;
      loading.value = false;
    });
  }, 100);
};

const onRefresh = () => {
  if (isTop.value) {
    toastLoading();
    store.commit("clearNews");
    getNews(store.state.navItem).then(() => {
      toast.clear();
      init("已成功刷新内容", "新闻").then(() => {});
    });
  }
};

toastLoading();
getNews(store.state.navItem).then(() => {
  toast.clear();
});

watch(navItem, (newVal) => {
  toastLoading();
  store.commit("clearNews");
  if (newVal !== "扫描") {
    getNews(newVal).then(() => {
      toast.clear();
    });
  }
});

watch(scanArray, (newVal) => {
  store.commit("clearNews");
  // 获取当前时间 yyyy年MM月dd日 HH时mm分ss秒
  const date = new Date();
  const nowTime = `${date.getHours()}时${date.getMinutes()}分${date.getSeconds()}秒`;
  const scanNews = {
    title: "图片提取内容",
    src: "",
    time: nowTime,
    content: "",
  };
  const contentArray = newVal.join("").split("。");
  for (let i = 0; i < contentArray.length; i += 1) {
    scanNews.content += `<p class="label-is-readable" label-is-readable="true">${contentArray[i]}。</p>`;
  }
  console.log(scanNews);
  store.commit("addNews", scanNews);
  isRe.value = true;
  isTop.value = false;
  toast.clear();
});

const onChange = (index) => {
  document
    .getElementsByClassName("wrapper")
    [index].addEventListener("scroll", (e) => {
      isTop.value = e.target.scrollTop === 0;
    });
  store.commit("changeActiveIndex", index);
  if (index + 3 >= store.state.news.data.length) {
    getNews(store.state.navItem);
  }
};
</script>
<template>
  <van-pull-refresh
    id="contentParent"
    v-model="loading"
    :disabled="!isTop"
    @refresh="onRefresh"
  >
    <van-swipe :loop="false" :show-indicators="false" @change="onChange">
      <van-swipe-item
        v-for="news in newsData"
        v-show="isRe"
        :key="news.title"
        indicator-color="white"
      >
        <content-typesetting :news="news" />
      </van-swipe-item>
    </van-swipe>
  </van-pull-refresh>
</template>
