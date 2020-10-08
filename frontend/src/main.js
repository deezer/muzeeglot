import Vue from 'vue'
import Muzeeglot from './Muzeeglot.vue'
import store from './store'
import vuetify from './plugins/vuetify';

Vue.config.productionTip = false

new Vue({
  store,
  vuetify,
  render: h => h(Muzeeglot)
}).$mount('#app')
