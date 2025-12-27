import { createRouter , createWebHashHistory } from 'vue-router'
import Home from '../components/HomePage.vue'
import user from '../components/UserDash.vue'
import loginpage from '../components/Login.vue'
import register from '@/components/Register.vue'
import partnersdash from '@/components/HospitalDash.vue'
import partnersreg from '@/components/HospitalReg.vue'
import partnerslogin from '@/components/HospitalLogin.vue'




const routes =[
    {
        path:'/',
        name: 'Home',
        component : Home,
        meta: { title :  'JeevanDaan+ | India’s Smart Blood Donation Platform' }
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
        path:'/partnersdash',
        name: 'partnersdash',
        component : partnersdash,
        meta: { hideFooter: true ,title: 'JeevanDaan+ | Partner'}

    },
    {
        path:'/partnersreg',
        name: 'partnersreg',
        component : partnersreg,
        meta: { hideFooter: true ,title: 'JeevanDaan+ | Partner | Register'}

    },
    {
        path:'/partners_login',
        name: 'partners_login',
        component : partnerslogin,
        meta: { hideFooter: true ,title: 'JeevanDaan+ | Partner | Login'}

    }

    


    

]

const router = createRouter ({
    history : createWebHashHistory(),
    routes

})
export default router