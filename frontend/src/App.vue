<script>
  import Header from './components/Header.vue';
  import Navbar from './components/Navbar.vue';
  import Footer from './components/Footer.vue';

  export default {
    data() {
      return {};
    },
    components: {
      Header,
      Navbar,
      Footer,
    },
  };
</script>

<template>
  <Header />
  <!-- <Navbar /> -->
   <div  class = 'flex-grow-1 align-items-center' >
    <router-view/>

   </div>
  <!-- <button class = 'btn btn-primary'>Click<i class="bi bi-bell-fill"></i></button> -->
  <Footer />
</template>

<style scoped></style>
