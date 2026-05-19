import '@mdi/font/css/materialdesignicons.css'
import 'vuetify/styles'
import '@jamescoyle/vue-icon'
import { createVuetify } from 'vuetify'

export default createVuetify({
  theme: {
    defaultTheme: 'light',
    themes: {
      light: {
        colors: {
          primary: '#1976D2', // Azul
          secondary: '#424242', // Gris oscuro
          accent: '#82B1FF', // Azul claro
          error: '#FF5252', // Rojo (ya usabas rojo en algunos botones)
          info: '#2196F3',
          success: '#4CAF50',
          warning: '#FFC107',
          background: '#f0f0f0', // Fondo general que usas en varias vistas
          surface: '#ffffff', // Fondo de tarjetas
        },
      },
    },
  },
})