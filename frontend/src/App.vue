<template>
  <div>
    <NavBar></NavBar>
    <IntroBox></IntroBox>
    <router-view></router-view>
  </div>
</template>

<script>
import NavBar from './components/NavBar'
import IntroBox from './components/IntroBox'

export default {
  components: { NavBar, IntroBox }
}
</script>

<style>

</style>