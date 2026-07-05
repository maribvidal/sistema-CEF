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
      dark: {
        colors: {
          primary: '#90caf9', // Azul más claro para modo oscuro
          secondary: '#bdbdbd', 
          accent: '#448aff', 
          error: '#ef5350', 
          info: '#29b6f6',
          success: '#66bb6a',
          warning: '#ffa726',
          background: '#121212', // Fondo oscuro
          surface: '#1e1e1e', // Fondo de tarjetas oscuro
        },
      },
    },
  },
})