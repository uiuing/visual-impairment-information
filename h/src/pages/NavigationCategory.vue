<script setup>
import { computed, ref, watch } from "vue";
import { useStore } from "vuex";

import imgToText from "../utils/api/image";
import { init } from "../utils/c/audio";
import newsCategoryS from "../utils/data/common";

const newsCategory = ref(newsCategoryS);

const store = useStore();
const active = computed(() => store.state.navItem);

const categoryChange = (category) => {
  store.commit("changeNavItem", category);
  return category;
};

const categoryToLeft = () => {
  const index = newsCategory.value.findIndex((item) => item === active.value);
  if (index < newsCategory.value.length - 1) {
    store.commit("changeNavItem", newsCategory.value[index + 1]);
  } else {
    store.commit("changeIsLoading", true);
    init(
      `当前是${active.value}频道，您可以试着从左往右滑动，切换至更多频道`,
      "新闻"
    ).then(() => {
      store.commit("changeIsLoading", false);
    });
  }
};
const categoryToRight = () => {
  const index = newsCategory.value.findIndex((item) => item === active.value);
  if (index > 0) {
    store.commit("changeNavItem", newsCategory.value[index - 1]);
  } else {
    store.commit("changeIsLoading", true);
    init(
      `当前是${active.value}频道，您可以试着从右往左滑动，切换至更多频道`,
      "新闻"
    ).then(() => {
      store.commit("changeIsLoading", false);
    });
  }
};

watch(active, (newVal) => {
  let tips = `已切换至${newVal}频道`;
  if (newVal === "扫描") {
    tips = "正在提取图片内容，自动为您切换至扫描频道";
  } else if (newsCategory.value.indexOf("扫描") !== -1) {
    newsCategory.value.shift();
  }
  store.commit("changeIsLoading", true);
  init(tips, "新闻").then(() => {
    store.commit("changeIsLoading", false);
  });
});

const afterRead = (file) => {
  if (newsCategory.value.indexOf("扫描") === -1) {
    newsCategory.value.unshift("扫描");
  }
  setTimeout(() => {
    document.querySelector("#van-tabs-1-0 > span").click();
  }, 100);
  imgToText(file.content).then((res) => {
    store.commit("changeScanArray", res);
  });
};
</script>
<template>
  <van-tabs
    v-touch:swipe.left="categoryToLeft"
    v-touch:swipe.right="categoryToRight"
    :active="active"
    :before-change="categoryChange"
  >
    <van-tab
      v-for="category in newsCategory"
      :key="category"
      :name="category"
      :title="category"
    >
    </van-tab>
    <van-uploader
      id="open-image"
      :after-read="afterRead"
      style="display: none"
    />
  </van-tabs>
</template>
