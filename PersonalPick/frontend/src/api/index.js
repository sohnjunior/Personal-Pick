import axios from 'axios';

axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';

function submitFile(formData) {
  return axios.post('http://127.0.0.1:8000/shopping/query/', formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  })
}

export { submitFile }