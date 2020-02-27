import Vue from 'vue'
import VueRouter from 'vue-router'
import ProductList from '../views/ProductList.vue'
import Main from '../views/Main.vue'

Vue.use(VueRouter);

export default new VueRouter({
  routes: [
    {
      path:'/',
      name: 'main',
      component: Main,
    },
    {
      path: '/products',
      name: 'products',
      component: ProductList,
    }
  ]
});