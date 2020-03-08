<template>
  <div>
    <b-container>
      검색 결과
    </b-container>
    <hr> 

    <b-container v-for="idx in productCount" :key="idx">
    <Product :index="idx"></Product><br>
    </b-container>

  </div>
</template>

<script>
import Product from '../components/Product';

export default {
  components: { Product },
  computed: {
    productCount() {
      return this.$store.getters.getProductCount;
    }
  }
}
</script>

<style scoped>
hr {
  width:90%
}
</style>