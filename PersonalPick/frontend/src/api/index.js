import axios from 'axios';

axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';

function submitFile(formData) {
  return axios.post('http://127.0.0.1:8000/shopping/query/', formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  })
}

function loginUser(userData) {
  return axios.post('http://127.0.0.1:8000/rest-auth/login/', userData);
}

function logoutUser() {
  return axios.post('http://127.0.0.1:8000/rest-auth/logout/');
}

export { submitFile, loginUser, logoutUser }