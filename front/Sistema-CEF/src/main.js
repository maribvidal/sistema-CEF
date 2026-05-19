import { createApp } from 'vue'
import { createPinia } from 'pinia'
import SvgIcon from '@jamescoyle/vue-icon'
import App from './App.vue'
import router from './router'
import vuetify from './plugins/vuetify'
import './assets/main.css'

const app = createApp(App)

// Registrar el componente SvgIcon globalmente para usarlo en cualquier lugar como <svg-icon />
app.component('svg-icon', SvgIcon)

app.use(createPinia())
app.use(router)
app.use(vuetify)

app.mount('#app')
