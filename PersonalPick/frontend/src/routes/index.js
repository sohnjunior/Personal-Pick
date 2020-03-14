import Vue from 'vue'
import VueRouter from 'vue-router'
import ProductList from '../views/ProductList.vue'
import MainPage from '../views/MainPage.vue'
import SignInPage from '../views/SignInPage.vue'
import CartPage from '../views/CartPage.vue'
import PageNotFound from '../views/NotFoundPage.vue'

Vue.use(VueRouter);

export default new VueRouter({
  routes: [
    {
      path:'/',
      name: 'main',
      component: MainPage,
    },
    {
      path: '/products',
      name: 'products',
      component: ProductList,
    },
    {
      path: '/signin',
      name: 'signin',
      component: SignInPage,
    },
    {
      path: '/cart',
      name: 'cart',
      component: CartPage,
    },
    {
      path: '*',
      name: 'notfound',
      component: PageNotFound,
    }
  ]
});