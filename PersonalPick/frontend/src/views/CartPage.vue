<template>
  <b-container>
    <h2>My Picks</h2>
    
    <b-table hover :items="items">
      <template v-slot:cell(image)="data">
        <b-img thumbnail fluid :src="data.value" alt="image" width="140px" height="140px"></b-img>
      </template>
      <template v-slot:cell(info)="data">
        <h6>{{ data.value.title }}</h6>
        <div class="mall-name">{{ data.value.mall }}</div>
        <div class="price-tag">
          <spen v-if="data.value.lowPrice !== '0'">{{ data.value.lowPrice }}</spen>
          <spen v-if="data.value.lowPrice !== data.value.highPrice && data.value.highPrice !== '0'"> ~ {{ data.value.highPrice }}</spen>
        </div>
      </template>
      <template v-slot:cell(link)="data">
        <div class="purchase-link">
          <a :href="data.value" target="_blank">구매하기</a>
        </div>
      </template>
    </b-table>
  </b-container>
</template>

<script>
import { getCart } from '../api/index'

export default {
  data() {
    return {
      productInfos: [],
      items: [],
    }
  },
  async created() {
    const { data } = await getCart();
    this.productInfos = data;
    for(let i = 0; i < this.productInfos.length; i++) {
      const obj = {
        'image': this.productInfos[i].image,
        'info': { 
          'title': this.productInfos[i].title, 
          'mall': this.productInfos[i].mallName,
          'lowPrice': this.productInfos[i].lprice,
          'highPrice': this.productInfos[i].hprice, 
        },
        'link': this.productInfos[i].link,
      };

      this.items.push(obj);
    }
  }
}
</script>

<style scoped>
h2 {
  margin-top: 15px;
  margin-bottom: 30px;
}
h6 {
  margin-top: 25px;
}
.mall-name {
  margin-top: 10px;
  margin-bottom: 10px;
  color: rgba(92, 94, 88, 0.918);
}
.price-tag {
  margin-top: 15px;
  font-size: 1.1rem;
}
.purchase-link {
  margin-top: 35px;
}
</style>