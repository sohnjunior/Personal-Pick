import Vue from 'vue';
import Vuex from 'vuex';

import { loginUser, logoutUser } from '../api';
import { getUserCookie, getAuthToken } from '../cookies';

Vue.use(Vuex);

const store = new Vuex.Store({
  state: {
    productInfoList: [],
    productCount: 0,

    userEmail: getUserCookie() || '',
    token: getAuthToken() || '',
  },
  getters: {
    getProductsInfo: state => {
      return state.productInfoList;
    },
    getProductCount: state => {
      return state.productInfoList.length;
    },
    isLoggedIn: state => {
      return state.userEmail !== '' ? true : false;
    }
  },
  mutations: {
    updateInfo(state, payload) {
      state.productInfoList = payload.infos;
    },
    setUserEmail(state, payload) {
      state.userEmail = payload.email;
    },
    setUserToken(state, payload) {
      state.token = payload.key;
    }
  },
  actions: {
    async userLogin({ commit }, loginData) {
      const { email, password } = loginData;

      const userData = {
        email: email,
        password: password
      };
      const { data, status } = await loginUser(userData);
      commit('setUserEmail', userData);
      commit('setUserToken', { key: data.key });
      return { key: data.key, status };
    },
    async userLogout({ commit }) {
      const response = await logoutUser();
      commit('setUserEmail', { email: '' });
      return response;
    },
  }
});

export default store;