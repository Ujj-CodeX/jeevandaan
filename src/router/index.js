import { createRouter , createWebHashHistory } from 'vue-router'
import Home from '../components/HomePage.vue'
import user from '../components/UserDash.vue'
import loginpage from '../components/Login.vue'
import register from '@/components/Register.vue'
import hospitaldash from '@/components/HospitalDash.vue'
import hospitalreg from '@/components/HospitalReg.vue'
import hospitallogin from '@/components/HospitalLogin.vue'




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

    },
    {
        path:'/hospitaldash',
        name: 'hospitaldash',
        component : hospitaldash,
        meta: { hideFooter: true ,title: 'JeevanDaan+ | Hospital'}

    },
    {
        path:'/hospitalreg',
        name: 'hospitalreg',
        component : hospitalreg,
        meta: { hideFooter: true ,title: 'JeevanDaan+ | Hospital | Register'}

    },
    {
        path:'/hospital_login',
        name: 'hospital_login',
        component : hospitallogin,
        meta: { hideFooter: true ,title: 'JeevanDaan+ | Hospital | Login'}

    }

    


    

]

const router = createRouter ({
    history : createWebHashHistory(),
    routes

})
export default router