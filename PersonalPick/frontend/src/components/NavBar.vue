<template>
  <div>
  <b-navbar toggleable="lg" type="light" variant="light" >
    <b-navbar-brand to="/">Personal Pick</b-navbar-brand>

    <b-navbar-nav class="ml-auto">
      <b-nav-item v-if="isLoggedIn" @click="openCart">찜목록</b-nav-item>
      <b-nav-item v-if="!isLoggedIn" @click="openLogin">로그인</b-nav-item>
      <b-nav-item v-if="isLoggedIn" @click="logoutUser"> 로그아웃</b-nav-item>
      <b-nav-item v-if="!isLoggedIn" to="/signin">회원가입</b-nav-item>
    </b-navbar-nav>
  </b-navbar>
  <LoginModal @login="closeLogin" @close="showModal=false" v-if="showModal"></LoginModal>
  </div>
</template>

<script>
import LoginModal from './LoginModal';
import { deleteCookie } from '../cookies';

export default {
    data() {
      return {
        showModal: false,
      }
    },
    components: {
      LoginModal,
    },
    computed: {
      isLoggedIn() {
        return this.$store.getters.isLoggedIn;
      }
    },
    methods: {
      openLogin() {
        this.showModal = true;
      },
      closeLogin() {
        this.showModal = false;
      },
      logoutUser() {
        const res = this.$store.dispatch('userLogout');
        console.log(res);
        deleteCookie('user_email');
        this.$router.push('/');
      },
      openCart() {
        this.$router.push('/cart');
      }
    },
}
</script>

<style>
</style>