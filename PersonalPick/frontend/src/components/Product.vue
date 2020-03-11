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
          <br>
          <br><b-link :href="productLink" target="_blank" class="card-link">구매링크</b-link>
        </b-card-body>
      </b-col>
    </b-row>
  </b-card>
</div>
</template>

<script>
export default {
  props: ['index', 'pageIndex', 'perPage'],
  computed: {
    idx() {
      return this.pageIndex * this.perPage + this.index - 1;
    },
    imageSrc() {
      return this.$store.getters.getProductsInfo[this.idx]['image'];
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
</style>