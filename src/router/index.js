import { createRouter , createWebHashHistory } from 'vue-router'
import Home from '../components/HomePage.vue'
import user from '../components/UserDash.vue'
import loginpage from '../components/Login.vue'
import register from '@/components/Register.vue'
import partnersdash from '@/components/HospitalDash.vue'
import partnersreg from '@/components/HospitalReg.vue'
import partnerslogin from '@/components/HospitalLogin.vue'
import request1 from '@/components/Request1.vue'
import learn from '@/components/Learn.vue'
import Chat from '@/components/Chat.vue'
import RequestSuccess from '@/components/RequestSuccess.vue'
import Profile from '@/components/Profile.vue'




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
        meta: { title: 'JeevanDaan+ | Partner'}

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

    },
    {
        path:'/user_request',
        name: 'request1',
        component : request1,
        meta: { title: 'JeevanDaan+ | Blood | Request'}

    },
    {
        path:'/learn',
        name: 'learn',
        component : learn,
        meta: { title: 'JeevanDaan+ | Learn'}
    },

    {
    path: '/chat/:id',
    name: 'Chat',
    component: Chat,
    meta: { title: 'JeevanDaan+ | Chat'}
  },
  {
        path: '/request-success',
        name: 'RequestSuccess',
        component: RequestSuccess
    },
    { path: '/profile', name: 'Profile', component: Profile, meta: { title: 'JeevanDaan+ | Profile'} }
    
    

]

const router = createRouter ({
    history : createWebHashHistory(),
    routes

})
export default router