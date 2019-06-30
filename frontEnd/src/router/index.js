import Vue from 'vue'
import Router from 'vue-router'
import index from '@/pages/index'
import login from '@/pages/login'
import apply from '@/pages/apply'
import myProject from '@/pages/myProject'
import firstTrial from '@/pages/firstTrial'
import addCompetition from '@/pages/addCompetition'
import announce from '@/pages/announce'
import competitionList from '@/pages/competitionList'
import professorManagement from '@/pages/professorManagement'
import projectReview from '@/pages/projectReview'
import projectDetail from '@/pages/projectDetail'
Vue.use(Router);

export default new Router({
    linkExactActiveClass:'active',
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
        {
            path: '/addCompetition',
            name: 'addCompetition',
            component: addCompetition,
        },
        {
            path: '/announce',
            name: 'announce',
            component: announce,
        },
        {
            path: '/competitionList',
            name: 'competitionList',
            component: competitionList,
        },
        {
            path: '/professorManagement',
            name: 'professorManagement',
            component: professorManagement,
        },
        {
            path: '/projectReview',
            name: 'projectReview',
            component: projectReview,
        },
        {
            path: '/projectDetail',
            name: 'projectDetail',
            component: projectDetail,
        },
  ]
})
