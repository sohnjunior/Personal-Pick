import axios from 'axios';

axios.defaults.baseURL = 'http://127.0.0.1:8000/';
axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';

function submitFile(formData) {
  return axios.post('shopping/query/', formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  })
}

function loginUser(userData) {
  return axios.post('rest-auth/login/', userData);
}

function logoutUser() {
  return axios.post('rest-auth/logout/');
}

function registerUser(userData) {
  return axios.post('rest-auth/registration/', userData);
}

function addCart(productData) {
  return axios.post('shopping/cart/', productData);
}

function getCart() {
  return axios.get('shopping/cart/');
}

function removeCartItem(productData) {
  return axios.delete("shopping/cart/", productData);
}

export { submitFile, loginUser, logoutUser, registerUser, addCart, getCart, removeCartItem }