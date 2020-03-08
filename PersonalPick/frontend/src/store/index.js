import Vue from 'vue';
import Vuex from 'vuex';

Vue.use(Vuex);

const store = new Vuex.Store({
  state: {
    productInfoList: [],
    productCount: 0,
  },
  getters: {
    getProductsInfo: state => {
      return state.productInfoList;
    },
    getProductCount: state => {
      return state.productInfoList.length;
    }
  },
  mutations: {
    updateInfo(state, payload) {
      state.productInfoList = payload.infos;
    },
  },
});

export default store;