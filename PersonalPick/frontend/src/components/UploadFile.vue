<template>
  <div>
    <b-form-file v-model="file" class="file-form" id="file" name="file" ref="file" capture="true" browse-text="파일선택" @change="handleFileUpload"></b-form-file> <br>
    <b-img thumbnail="" alt="사용자 입력 이미지" blank="true" width="350" height="350" rounded="true" src=""></b-img>
    <b-button pill variant="outline-secondary" size="lg" type="submit" @click="submitFile">결과보기</b-button>
  </div>
</template>

<script>
  import axios from 'axios'

  axios.defaults.xsrfCookieName = 'csrftoken';
  axios.defaults.xsrfHeaderName = 'X-CSRFToken';

export default {
  data() {
    return {
      file: null
    }
  },
  methods: {
    submitFile() {
      let formData = new FormData();
      formData.append('file', this.file);

      axios.post('http://localhost:8000/shopping/query/', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      }).then((res) => {
        console.log(res);
      }).catch((err) => {
        console.log(err);
      });
    },
    handleFileUpload() {
      this.file = this.$refs.file.files[0];
    }
  }
}
</script>

<style scoped>
.file-form {
  width: 45%;
}
</style>