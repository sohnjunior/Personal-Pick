<template>
  <b-container>
    <h2>My Picks</h2>
    
    <b-table ref="table" hover :items="items">
      <template v-slot:cell(image)="data">
        <b-img thumbnail fluid :src="data.value" alt="image" width="140px" height="140px"></b-img>
      </template>
      <template v-slot:cell(info)="data">
        <h6>{{ data.value.title }}</h6>
        <div class="mall-name">{{ data.value.mall }}</div>
        <div class="price-tag">
          <span v-if="data.value.lowPrice !== '0'">{{ data.value.lowPrice }}</span>
          <span v-if="data.value.lowPrice !== data.value.highPrice && data.value.highPrice !== '0'"> ~ {{ data.value.highPrice }}</span>
        </div>
      </template>
      <template v-slot:cell(etc)="data">
        <div class="purchase-link">
          <b-col>
            <b-row>
              <a :href="data.value.link" target="_blank">구매하기</a>
            </b-row>
            <b-row>
              <button class="delete-item" @click="deleteItem(data.value.id, data.index)"><BIconTrashFill/>삭제</button>
            </b-row>
          </b-col>
        </div>
      </template>
    </b-table>
  </b-container>
</template>

<script>
import { getCart, removeCartItem } from '../api/index'
import { BIconTrashFill } from 'bootstrap-vue'

export default {
  data() {
    return {
      productInfos: [],
      items: [],
    }
  },
  components: { BIconTrashFill },
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
        'etc': {
          'id': this.productInfos[i].id,
          'link': this.productInfos[i].link,
        }
      };

      this.items.push(obj);
    }
  },
  methods: {
    async deleteItem(id, idx) {
      // remove item
      const productData = {
        data: { id: id }
      };
      this.items.splice(idx, 1);
      const response = await removeCartItem(productData);

      // refresh
      this.$refs.table.refresh();
      console.log(response);
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
.delete-item {
  background-color: transparent;
  color: rgba(196, 38, 38, 0.815);
  border: 0;
  outline: 0;
}
</style>