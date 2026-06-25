import { createApp } from 'vue'
import { createPinia } from 'pinia'
import SvgIcon from '@jamescoyle/vue-icon'
import App from './App.vue'
import router from './router'
import vuetify from './plugins/vuetify'
import { initAuth } from './services/UsuariosServices.js'
import './assets/main.css'
import './assets/base.css'

const app = createApp(App)

// Registrar el componente SvgIcon globalmente para usarlo en cualquier lugar como <svg-icon />
app.component('svg-icon', SvgIcon)

app.use(createPinia())
app.use(router)
app.use(vuetify)

// Inicializar autenticación desde token guardado en localStorage
initAuth()

app.mount('#app')
