<template>
<main class="container-fluid">
      <router-view />  
    </main>
    
   <Footer v-if="!$route.meta.hideFooter" />
  
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


