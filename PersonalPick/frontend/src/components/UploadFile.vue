<template>
  <div>
    <input type="file" id="file" name="file" ref="file" @change="handleFileUpload">
    <button type="submit" @click="submitFile">제출</button>
  </div>
</template>

<script>
  import axios from 'axios'

  axios.defaults.xsrfCookieName = 'csrftoken';
  axios.defaults.xsrfHeaderName = 'X-CSRFToken';

export default {
    methods: {
        submitFile() {
            let formData = new FormData();
                   formData.append('file', this.file);

                   axios.post('http://localhost:8000/shopping/query/', formData, {
                       headers: { 'Content-Type': 'multipart/form-data' }
                   })
                   .then((res) => {
                       console.log(res);
                   })
                   .catch((err) => {
                      console.log(err);
                   });
        },
        handleFileUpload() {
            this.file = this.$refs.file.files[0];
        }
    }
}
</script>

<style>

</style>