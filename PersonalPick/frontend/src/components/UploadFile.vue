<template>
  <div>
    <div class="file-upload-form">
      <b-form-file v-model="imageData" id="file" ref="file" browse-text="파일선택" @change="handleFileUpload"></b-form-file>
    </div> <br>
    <div>
      <b-img thumbnail :src="imagePreview" class="preview-image" block rounded></b-img>
    </div> <br>
    <div>
      <b-button pill variant="outline-secondary" size="lg" type="submit" @click="submitFile">결과보기</b-button>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';

const base64Encode = data =>
  new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.readAsDataURL(data);
    reader.onload = () => resolve(reader.result);
    reader.onerror = error => reject(error);
  });

export default {
  data() {
    return {
      imageData: null,
      imagePreview: null
    }
  },
  watch: {
      imageData(newValue, oldValue) {
        if(newValue !== oldValue) {
          if(newValue) {
            base64Encode(newValue)
            .then(value => {
              this.imagePreview = value;
            })
            .catch(() => {
              this.imagePreview = null;
            });
          } else {
            this.imagePreview = null;
          }
        }
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
    }
  }
}
</script>

<style scoped>
.file-upload-form {
  width: 25%;
  margin: auto;
}
.preview-image {
  width: 300px;
  height: 300px;
  margin: auto;
}
</style>