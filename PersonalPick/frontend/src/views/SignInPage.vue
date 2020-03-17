<template>
  <b-container>
    <h2>Join us!</h2>

    <b-container>
      <b-form  @submit.stop.prevent>
        <b-form-group label="Email address">
          <b-form-input v-model="email" :state="emailValidation" type="email" aria-describedby="email-feedback"></b-form-input>
          <b-form-invalid-feedback id="email-feedback">
            이메일 형식에 맞게 입력해주세요.
          </b-form-invalid-feedback>
        </b-form-group>

        <b-form-group label="Nickname">
          <b-form-input v-model="nickname" :state="nicknameValidation" type="text" aria-describedby="nickname-feedback"></b-form-input>
          <b-form-invalid-feedback id="nickname-feedback">
            사용할 닉네임을 입력하세요.
          </b-form-invalid-feedback>
        </b-form-group>
        
        <b-form-group label="Password">
          <b-form-input v-model="password1" :state="passwordValidation" type="password" aria-describedby="password1-feedback"></b-form-input>
          <b-form-invalid-feedback id="password1-feedback">
            비밀번호는 8~15자의 영문과 최소한 하나의 숫자와 특수문자를 포함해야 합니다.
          </b-form-invalid-feedback>
        </b-form-group>

        <b-form-group label="Password confirm">
          <b-form-input v-model="password2" :state="passwordConfirmValidation" type="password" aria-describedby="password2-feedback"></b-form-input>
          <b-form-invalid-feedback id="password2-feedback">
            비밀번호가 일치하지 않습니다.
          </b-form-invalid-feedback>
        </b-form-group>

        <b-form-group label="Date of birth">
          <b-form-input v-model="birthDay" type="date"></b-form-input>
        </b-form-group>

        <b-form-group label="Gender">
          <b-form-radio-group v-model="gender" :options="options">
          </b-form-radio-group>
        </b-form-group>

        <button class="submit-button" @click="registerUser">
          가입 하기
        </button>
      </b-form>
    </b-container>
  </b-container>
</template>

<script>
import { registerUser } from '../api/index';

export default {
  data() {
    return {
      email: '',
      nickname: '',
      password1: '',
      password2: '',
      birthDay: '',
      gender: 'm',
      options: [
        { text: '남성', value: 'm' },
        { text: '여성', value: 'f' },
      ]
    }
  },
  computed: {
    emailValidation() {
      const pattern = /^\w+@[a-zA-Z_]+?\.[a-zA-Z]{2,3}$/; 
      return this.email.match(pattern) ? true : false;
    },
    nicknameValidation() {
      return (this.nickname !== '') ? true : false;
    },
    passwordValidation() {
      const pattern =  /^(?=.*[0-9])(?=.*[!@#$%^&*])[a-zA-Z0-9!@#$%^&*]{8,15}$/;
      if(this.password1.match(pattern)) {
        return true;
      } else {
        return false;
      }
    },
    passwordConfirmValidation() {
      // 유효한 비밀번호인지 먼저 확인한다
      if(!this.passwordValidation) {
        return false;
      }
      // 만약 비밀번호가 같지 않다면 false
      return (this.password1 === this.password2) ? true : false;
    }
  },
  methods: {
    async registerUser() {
      // 유저 정보 json 생성
      const userData = {
         email: this.email,
         password1: this.password1,
         password2: this.password2,
         nickname: this.nickname,
         date_of_birth: this.birthDay,
         gender: this.gender,
      };

      // 백엔드 API 호출
      const response = await registerUser(userData);
      console.log(response.status);
      this.makeToast('회원가입이 완료되었습니다!');
      this.$router.push('/');
    },
    makeToast(message) {
      this.$root.$bvToast.toast(message, {
        title: '알림',
        variant: 'success',
        autoHideDelay: 1500,
        appendToast: true
      })
    }
  }
}
</script>

<style scoped>
h2 {
  font-family: 'Comic Sans MS';
  margin-top: 40px;
  margin-bottom: 20px;
}

.submit-button {
  border-top-left-radius: 3px;
  border-top-right-radius: 3px;
  border-bottom-left-radius: 3px;
  border-bottom-right-radius: 3px;
  border: 0;
  outline: 0;
  margin-top: 30px;
  margin-bottom: 90px;
  width: 200px;
  height: 40px;
  color: white;
  background-color: #42b977e0;
}

.submit-button:hover {
  background-color: #46b176e0;
}

.submit-button:active {
  background-color: #46b176e0;
  transform: translateY(3px);
}
</style>