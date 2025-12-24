import { createRouter , createWebHashHistory } from 'vue-router'
import Home from '../components/HomePage.vue'
import user from '../components/UserDash.vue'
const routes =[
    {
        path:'/',
        name: 'Home',
        component : Home
    },
    {
        path:'/User',
        name: 'user',
        component : user
    }

    

]

const router = createRouter ({
    history : createWebHashHistory(),
    routes

})
export default router