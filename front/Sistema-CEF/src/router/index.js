import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('../views/HomeView.vue'),
    },
    {
      path: '/inicioSesion',
      name: 'inicioSesion',
      component: () => import('../views/UsuarioVisitante/InicioSesionView.vue'),
    },
    {
      path: '/recuperar-contraseña',
      name: 'recuperarContraseña',
      component: () => import('../views/UsuarioVisitante/RecuperarContraseña.vue'),
    },
    {
      path: '/registro',
      name: 'registro',
      component: () => import('../views/UsuarioVisitante/Registro.vue'),
    }
  ],
})

export default router
