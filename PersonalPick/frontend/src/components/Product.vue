<template>
<div>
  <b-card class="product-info">
    <b-row>
      <b-col md="5">
        <b-card-img :src="imageSrc" height="200"></b-card-img>
      </b-col>
      <b-col md="6">
        <b-card-body :title="productTitle" title-tag="h5" :sub-title="productMallName" sub-title-tag="h6">
          <br><b-link :href="productLink" target="_blank" class="card-link">구매하러 가기</b-link>
        </b-card-body>
      </b-col>
    </b-row>
  </b-card>
</div>
</template>

<script>
export default {
  props: ['index'],
  computed: {
    imageSrc() {
      return this.$store.getters.getProductsInfo[this.index-1]['image'];
    },
    productTitle() {
      return this.$store.getters.getProductsInfo[this.index-1]['title'];
    },
    productMallName() {
      return this.$store.getters.getProductsInfo[this.index-1]['mallName'];
    },
    productLink() {
      return this.$store.getters.getProductsInfo[this.index-1]['link'];
    },
  }
}
</script>

<style scoped>
.product-info {
  width: 700px;
  box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2);
}
.product-info:hover {
  box-shadow: 0 8px 16px 0 rgba(0,0,0,0.2);
}
</style>