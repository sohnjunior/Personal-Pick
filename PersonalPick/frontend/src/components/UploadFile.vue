<template>
  <div>
    <div class="file-upload-form">
      <b-form-file v-model="imageData" id="file" ref="file" browse-text="파일선택" @change="handleFileUpload"></b-form-file>
    </div> <br>
    <div class="preview-image">
      <img v-bind:src="imagePreview"/>
      <!--
      <b-img thumbnail alt="사용자 입력 이미지" blank="true" width="300" height="300" rounded="true" v-bind:src="imagePreview"></b-img>
      -->
    </div> <hr>
    <div class="input-button">
      <b-button pill variant="outline-secondary" size="lg" type="submit" @click="submitFile">결과보기</b-button>
    </div>
  </div>
</template>

<script>
  import axios from 'axios'

  axios.defaults.xsrfCookieName = 'csrftoken';
  axios.defaults.xsrfHeaderName = 'X-CSRFToken';

export default {
  data() {
    return {
      imageData: "",
      imagePreview: ""
    }
  },
  methods: {
    submitFile() {
      let formData = new FormData();
      formData.append('file', this.imageData);

      axios.post('http://localhost:8000/shopping/query/', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      }).then((res) => {
        console.log(res);
      }).catch((err) => {
        console.log(err);
      });
    },
    handleFileUpload() {
      this.imageData = this.$refs.file.files[0];
      
      // TODO handle preview image
      const reader = new FileReader();
      const vm = this;

      reader.onload = (e) => { vm.imagePreview = e.target.result; };
      reader.readAsDataURL(this.imageData);
    }
  }
}
</script>

<style scoped>
.file-upload-form {
  width: 25%;
  margin: auto;
}
</style>