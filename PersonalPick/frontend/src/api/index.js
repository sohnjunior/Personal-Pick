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

function registerUser(userData) {
  return axios.post('http://127.0.0.1:8000/rest-auth/registration/', userData);
}

function addCart(productData) {
  return axios.post('http://127.0.0.1:8000/shopping/cart/', productData);
}

function getCart() {
  return axios.get('http://127.0.0.1:8000/shopping/cart/');
}

function removeCartItem(productData) {
  return axios.delete("http://127.0.0.1:8000/shopping/cart/", productData);
}

export { submitFile, loginUser, logoutUser, registerUser, addCart, getCart, removeCartItem }