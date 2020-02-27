<template>
  <div>
    <b-container>
      분류된 카테고리 : 신발
    </b-container>
    <hr> 

    <b-container v-for="n in 5" v-bind:key="n">
      <b-card class="product-info">
        <b-row>
          <b-col md="6">
            <b-card-img src="https://picsum.photos/400/400/?image=20" width="100" height="150"></b-card-img>
          </b-col>
          <b-col md="6">
            <b-card-body title="상품명" sub-title="판매 회사명" >
              <b-card-text>{{n}}상품 설명</b-card-text>
              <b-link href="#" class="card-link">구매하러 가기</b-link>
            </b-card-body>
          </b-col>
        </b-row>
      </b-card>
      <br>
    </b-container>

  </div>
</template>

<script>
export default {}
</script>

<style scoped>
hr {
  width:90%
}
.product-info {
  width: 70%;
  box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2);
}
.product-info:hover {
  box-shadow: 0 8px 16px 0 rgba(0,0,0,0.2);
}
</style>