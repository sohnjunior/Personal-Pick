<template>
 <transition name="modal">
    <div class="modal-mask">
      <div class="modal-wrapper" @click="$emit('close')">
        <div class="modal-container">

          <div class="modal-header">
            <slot name="header">
              <h3>SIGN IN</h3>
            </slot>
          </div>

          <div class="modal-body">
            <b-form-group>
            <b-form-input
              v-model="email"
              type="email"
              :state="emailState"
              aria-describedby="email-feedback"
              placeholder="Email"
              autofocus
              trim
            ></b-form-input>
            <b-form-invalid-feedback id="email-feedback">
              이메일을 입력하세요
            </b-form-invalid-feedback>
            </b-form-group>
            
            <b-form-group>
            <b-form-input
              v-model="password"
              type="password"
              :state="passwordState"
              aria-describedby="password-feedback"
              placeholder="Password"
              trim
            ></b-form-input>
            <b-form-invalid-feedback id="password-feedback">
              비밀번호를 입력하세요
            </b-form-invalid-feedback>
            </b-form-group>
            
            <button class="modal-default-button" @click="clickButton" @keyup.enter="clickButton">
              로그인
            </button>
          </div>
        </div>
      </div>
    </div>
  </transition>
</template>

<script>
import { setUserCookie } from '../cookies';

export default {
  data() {
    return {
      email: '',
      password: ''
    }
  },
  computed: {
    emailState() {
      const pattern = /^\w+@[a-zA-Z_]+?\.[a-zA-Z]{2,3}$/; 
      return this.email.match(pattern) ? true : false;
    },
    passwordState() {
      return (this.password === '') ? false: true;
    },
  },
  methods: {
    clickButton() {
      const res = this.$store.dispatch('userLogin', {
        email: this.email,
        password: this.password,
      });
      setUserCookie(this.email);
      console.log(res);
      this.$emit('login');
    }
  }
}
</script>

<style scoped>
.modal-mask {
  position: fixed;
  z-index: 9998;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, .5);
  display: table;
  transition: opacity .3s ease;
}

.modal-wrapper {
  display: table-cell;
  vertical-align: middle;
}

.modal-container {
  width: 400px;
  margin: 0px auto;
  padding: 20px 30px;
  background-color: #fff;
  border-radius: 2px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, .33);
  transition: all .3s ease;
  font-family: Helvetica, Arial, sans-serif;
}

.modal-header h3 {
  margin-top: 0;
  color: #42b977e0;
}

.modal-body {
  margin: 15px 0;
}

.modal-default-button {
  border-top-left-radius: 3px;
  border-top-right-radius: 3px;
  border-bottom-left-radius: 3px;
  border-bottom-right-radius: 3px;
  border: 0;
  outline: 0;
  margin-top: 30px;
  width: 308px;
  height: 40px;
  color: white;
  background-color: #42b977e0;
}

.modal-default-button:hover {
  background-color: #46b176e0;
}

.modal-default-button:active {
  background-color: #46b176e0;
  transform: translateY(3px);
}

/*
 * The following styles are auto-applied to elements with
 * transition="modal" when their visibility is toggled
 * by Vue.js.
 *
 * You can easily play with the modal transition by editing
 * these styles.
 */

.modal-enter {
  opacity: 0;
}

.modal-leave-active {
  opacity: 0;
}

.modal-enter .modal-container,
.modal-leave-active .modal-container {
  -webkit-transform: scale(1.1);
  transform: scale(1.1);
}
</style>