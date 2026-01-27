<script>
  import Header from './components/Header.vue';
  import Footer from './components/Footer.vue';

  export default {
    data() {
      return {};
    },
    components: {
      Header,
      Footer,
    },
  };
</script>

<template>
  <Header />
   <div  class = 'd-flex flex-grow-1 align-items-center' >
    <router-view/>
   </div>
  <Footer />
</template>

<style scoped></style>
