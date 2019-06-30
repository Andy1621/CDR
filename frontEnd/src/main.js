// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import iView from 'iview';
import 'iview/dist/styles/iview.css';
import VueResource from 'vue-resource';
import cookie from 'js-cookie'

import '../static/css/bootstrap.min.css'
import '../static/css/style.css'
import '../static/css/main.css'

import $ from 'jquery/dist/jquery.min'
import $$ from 'bootstrap/dist/js/bootstrap.min.js'

Vue.use(iView);
Vue.use(VueResource)

Vue.config.productionTip = false;

Vue.prototype.$baseURL = 'http://127.0.0.1:5000';
Vue.prototype.$cookie =cookie;

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>'
});
Vue.prototype.$Notice.config({
  top: 90,
  duration: 3
});
