import axios from 'axios';
import store from '../store';

const instance = axios.create({
  baseURL: 'http://ec2-3-34-48-227.ap-northeast-2.compute.amazonaws.com/',
  xsrfCookieName: 'csrftoken',
  xsrfHeaderName: 'X-CSRFToken',
});

// axios delete 수행 시 header에 포함이 안되서 새로운 인스턴스 생성
const newInstance = axios.create({
  baseURL: 'http://ec2-3-34-48-227.ap-northeast-2.compute.amazonaws.com/',
  xsrfCookieName: 'csrftoken',
  xsrfHeaderName: 'X-CSRFToken',
});
newInstance.defaults.headers.common['Authorization'] = `TOKEN ${store.state.token}`;

function submitFile(formData) {
  return instance.post('shopping/query/', formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  })
}

function loginUser(userData) {
  return instance.post('rest-auth/login/', userData);
}

function logoutUser() {
  return instance.post('rest-auth/logout/');
}

function registerUser(userData) {
  return instance.post('rest-auth/registration/', userData);
}

function addCart(productData) {
  return instance.post('shopping/cart/', productData, {
    headers: { 'Authorization': `TOKEN ${store.state.token}` }
  });
}

function getCart() {
  return instance.get('shopping/cart/', {
    headers: { 'Authorization': `TOKEN ${store.state.token}` }
  });
}

function removeCartItem(productData) {
  return newInstance.delete("shopping/cart/", productData);
}

export { submitFile, loginUser, logoutUser, registerUser, addCart, getCart, removeCartItem }