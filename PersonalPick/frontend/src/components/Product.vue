<template>
<div>
  <b-card class="product-info">
    <b-row>
      <b-col md="5">
        <b-card-img-lazy :src="imageSrc" height="200"></b-card-img-lazy>
      </b-col>
      <b-col md="6">
        <b-card-body :title="productTitle" title-tag="h5" :sub-title="productMallName" sub-title-tag="h6">
          <br>
          <span class="price-text" v-if="productLowPrice != 0">{{ productLowPrice | currancy }}</span>
          <span class="price-text" v-if="productLowPrice < productHighPrice && productHighPrice != 0"> ~ {{ productHighPrice | currancy }}</span>
          <br><br>
          <b-link :href="productLink" target="_blank" class="card-link">구매링크</b-link>
          <button class="shopping-basket" @click="addCart" :disabled="!isLoggedIn"><BIconBucketFill/>담기</button>
        </b-card-body>
      </b-col>
    </b-row>
  </b-card>
</div>
</template>

<script>
import { addCart } from '../api/index';
import { BIconBucketFill } from 'bootstrap-vue';

export default {
  props: ['index', 'pageIndex', 'perPage'],
  components: {
    BIconBucketFill,
  },
  computed: {
    isLoggedIn() {
      return this.$store.getters.isLoggedIn;
    },
    idx() {
      return this.pageIndex * this.perPage + this.index - 1;
    },
    imageSrc() {
      return this.$store.getters.getProductsInfo[this.idx]['image'];
    },
    productId() {
      return this.$store.getters.getProductsInfo[this.idx]['id'];
    },
    productTitle() {
      return this.$store.getters.getProductsInfo[this.idx]['title'];
    },
    productMallName() {
      return this.$store.getters.getProductsInfo[this.idx]['mallName'];
    },
    productLink() {
      return this.$store.getters.getProductsInfo[this.idx]['link'];
    },
    productLowPrice() {
      return this.$store.getters.getProductsInfo[this.idx]['lprice'];
    },
    productHighPrice() {
      return this.$store.getters.getProductsInfo[this.idx]['hprice'];
    },
  },
  filters: {
    currancy(value) {
      return new Intl.NumberFormat().format(value);
    }
  },
  methods: {
    async addCart() {
      if(!this.isLoggedIn) {
        return;
      }
      const productData = {
        id: this.productId
      };
      const response = await addCart(productData);
      console.log(response);
      this.makeToast('장바구니에 추가되었습니다');
    },
    makeToast(message) {
      this.$root.$bvToast.toast(message, {
        title: '알림',
        variant: 'info',
        autoHideDelay: 1500,
        appendToast: true
      })
    }
  }
}
</script>

<style scoped>
.product-info {
  width: 33rem;
  box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2);
}
.product-info:hover {
  box-shadow: 0 8px 16px 0 rgba(0,0,0,0.2);
}
.price-text {
  font-family: 'Comic Sans MS';
  font-size: 1.20rem;
  color: rgba(228, 115, 23, 0.781);
}
.shopping-basket {
  color: rgba(100, 156, 209, 0.705);
  font-size: 1.1rem;
  margin-left: 2rem;
  background-color: #ffffff;
  border: 0;
  outline: 0;
}
</style>