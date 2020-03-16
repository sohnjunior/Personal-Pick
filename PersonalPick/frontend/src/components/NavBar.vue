<template>
  <div>
  <b-navbar toggleable="lg" type="light" variant="light">
    <b-navbar-brand class="brand-title" to="/">Personal Pick</b-navbar-brand>

    <b-navbar-nav class="ml-auto">
      <b-button variant="outline-success" v-if="isLoggedIn" @click="openCart">
        장바구니
      </b-button>
      <b-button variant="outline-success" v-if="!isLoggedIn" to="/signin">
        회원가입
      </b-button>
      <b-col>
        <b-button variant="outline-success" v-if="!isLoggedIn" @click="openLogin">
          로그인
        </b-button>
        <b-button variant="outline-danger" v-if="isLoggedIn" @click="logoutUser">
          로그아웃
        </b-button>
      </b-col>
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
        const response = this.$store.dispatch('userLogout');
        console.log(response);
        deleteCookie('user_email');
        this.$router.push('/');
      },
      openCart() {
        this.$router.push('/cart');
      },
    },
}
</script>

<style scoped>
.brand-title {
  font-family: 'Comic Sans MS';
  font-size: 1.20rem;
}
</style>