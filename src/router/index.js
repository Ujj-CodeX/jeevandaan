import { createRouter , createWebHashHistory } from 'vue-router'
import Home from '../components/HomePage.vue'
import user from '../components/UserDash.vue'
import loginpage from '../components/Login.vue'
import register from '@/components/Register.vue'
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
    },
    {
        path:'/login',
        name: 'login',
        component : loginpage,
        meta: { hideFooter: true ,title: 'JeevanDaan+ | Login'}
    },
    {
        path:'/register',
        name: 'register',
        component : register,
        meta: { hideFooter: true ,title: 'JeevanDaan+ | Register'}

    }
    


    

]

const router = createRouter ({
    history : createWebHashHistory(),
    routes

})
export default router