import Vue from 'vue'
import Router from 'vue-router'
import index from '@/pages/index'
import login from '@/pages/login'
import apply from '@/pages/apply'
import myProject from '@/pages/myProject'
import firstTrial from '@/pages/firstTrial'
Vue.use(Router)

export default new Router({
    routes: [
    {
        path: '/',
        name: 'login',
        component: login
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
    },
    {
        path: '/myProject',
        name: 'myProject',
        component: myProject,
    },
      {
        path: '/firstTrial',
        name: 'firstTrial',
        component: firstTrial,
      },
  ]
})
