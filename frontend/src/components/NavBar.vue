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
        this.$store.dispatch('userLogout');
        
        deleteCookie('user_email');
        deleteCookie('user_token');
        this.makeToast('로그아웃 되었습니다.');

        // 메인 페이지에서 로그아웃 하는 경우에 대한 예외처리 추가
        this.$router.push('/').catch(error => {
          if(error.name != 'NavigationDuplicated') {
            throw error;
          }
        });
      },
      openCart() {
        this.$router.push('/cart');
      },
      makeToast(message) {
        this.$root.$bvToast.toast(message, {
          title: '알림',
          variant: 'success',
          autoHideDelay: 1000,
          appendToast: true
        })
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