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
    }
  ],
})

export default router
