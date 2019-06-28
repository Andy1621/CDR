import Vue from 'vue'
import Router from 'vue-router'
import index from '@/pages/index'
import login from '@/pages/login'
import apply from '@/pages/apply'

Vue.use(Router)

export default new Router({
    routes: [
    {
        path: '/',
        name: 'login',
        component: index
    },
    {
        path: '/index',
        name: 'index',
        component: index,
    },
    {
        path: '/apply',
        name: 'apply',
        component: apply,
    }
  ]
})
