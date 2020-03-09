<template>
  <div>
    <b-container>
      <h2>검색 결과</h2>
    </b-container>
    <hr>

    <b-container>
      <b-row align-h="center">
        <b-col v-for="idx in firstRowCount" :key="idx">
          <Product :index="idx" :pageIndex="currentPage - 1" :perPage="imagePerPage"></Product>
        </b-col>
      </b-row> 
      <br>
      <b-row v-if="secondRowCount" align-h="center">
        <b-col v-for="idx in secondRowCount" :key="idx">
          <Product :index="idx + 2" :pageIndex="currentPage - 1" :perPage="imagePerPage"></Product>
        </b-col>
      </b-row>
    </b-container>

    <hr>
    <b-container class="pagination-bar">
      <b-pagination v-model="currentPage" :total-rows="productCount" :per-page="imagePerPage"></b-pagination>
    </b-container>
  </div>
</template>

<script>
import Product from '../components/Product';

export default {
  components: { Product },
  data () {
    return {
      currentPage: 1,
      imagePerPage: 4,
    }
  },
  computed: {
    perPage() {
      let ret = 0;
      if(this.productCount >= this.currentPage * this.imagePerPage) {
        ret = this.imagePerPage;
      } else {
        ret = this.productCount % this.imagePerPage;
      }
      
      return ret;
    },
    firstRowCount() {
      return (this.perPage >= 2 ? 2 : 1);
    },
    secondRowCount() {
      if(this.perPage <= 2) {
        return 0;
      } else if(this.perPage == 3) {
        return 1;
      } else {
        return 2;
      }
    },
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
.product-list {
  margin: 0 auto;
}
.pagination-bar {
  width: 10rem;
  margin: 0 auto;
}
</style>