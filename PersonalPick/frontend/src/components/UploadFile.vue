<template>
  <div>
    <div class="file-upload-form">
      <b-form-file v-model="imageData" id="file" ref="file" browse-text="파일선택"></b-form-file>
    </div> <br>
    <div>
      <b-img thumbnail :src="imagePreview" class="preview-image" block rounded></b-img>
    </div> <br>
    <div>
      <b-button type="submit" pill variant="outline-secondary" size="lg" class="submit-button" block @click="submitFile">결과보기</b-button>
    </div>
  </div>
</template>

<script>
import { submitFile } from '../api/index';

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
    async submitFile() {
      // if file not exist
      if(!this.imageData) {
        alert('파일 첨부가 필요합니다');
        return;
      }
      
      let formData = new FormData();
      formData.append('file', this.imageData);
      const response = await submitFile(formData);
      
      this.$store.commit('updateInfo', {infos: response.data});
      this.$router.push({name: 'products'});
    },
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
.submit-button {
  width: 20%;
  margin: 0 auto;
}
</style>