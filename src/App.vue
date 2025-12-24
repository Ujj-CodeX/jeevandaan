<template>
<main class="container-fluid">
      <router-view />  
    </main>
    
    <Footer />
  
</template>

<script>
import Footer from './components/Footer.vue'

export default {
  name: 'App',
  components: {
    Footer
  }
}
</script>


