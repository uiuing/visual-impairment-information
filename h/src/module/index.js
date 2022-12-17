import { createStore } from "vuex";

const store = createStore({
  state() {
    return {
      navItem: "头条",
      news: {
        activeIndex: 0,
        data: [],
      },
      newsOK: false,
      isPlay: false,
      isClose: false,
      isLoading: false,
      isPlayAll: false,
      isPlayAllPageFlag: false,
      playContent: "",
      scanArray: [],
    };
  },
  mutations: {
    changeNavItem(state, navItem) {
      // eslint-disable-next-line no-param-reassign
      state.navItem = navItem;
    },
    changeActiveIndex(state, index) {
      // eslint-disable-next-line no-param-reassign
      state.news.activeIndex = index;
    },
    addNews(state, news) {
      state.news.data.push(news);
    },
    clearNews(state) {
      // eslint-disable-next-line no-param-reassign
      state.news.data = [];
    },
    changeNewsOK(state, newsOK) {
      // eslint-disable-next-line no-param-reassign
      state.newsOK = newsOK;
    },
    changeIsPlay(state, isPlay) {
      // eslint-disable-next-line no-param-reassign
      state.isPlay = isPlay;
    },
    changePlayContent(state, playContent) {
      // eslint-disable-next-line no-param-reassign
      state.playContent = playContent;
    },
    changeIsClose(state, isClose) {
      // eslint-disable-next-line no-param-reassign
      state.isClose = isClose;
    },
    changeIsLoading(state, isLoading) {
      // eslint-disable-next-line no-param-reassign
      state.isLoading = isLoading;
    },
    changeIsPlayAll(state, isPlayAll) {
      // eslint-disable-next-line no-param-reassign
      state.isPlayAll = isPlayAll;
    },
    changeIsPlayAllPageFlag(state, isPlayAllPageFlag) {
      // eslint-disable-next-line no-param-reassign
      state.isPlayAllPageFlag = isPlayAllPageFlag;
    },
    changeScanArray(state, scanArray) {
      // eslint-disable-next-line no-param-reassign
      state.scanArray = scanArray;
    },
  },
});

export default store;
