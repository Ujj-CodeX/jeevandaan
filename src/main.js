import { createApp } from 'vue';
import App from './App.vue';
import router from './router';

router.beforeEach((to, from, next) => {
  const defaultTitle = 'JeevanDaan+'
  document.title = to.meta.title || defaultTitle
  next()
})

const app = createApp(App);

app.use(router);

app.mount('#app');
