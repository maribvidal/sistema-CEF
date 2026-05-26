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
    },
    {
      path: '/clases',
      name: 'clases',
      component: () => import('../views/UsuarioVisitante/ClassesView.vue'),
    },
    {
      path: '/perfil/:id',
      name: 'perfil',
      component: () => import('../views/UsuarioCliente/PerfilView.vue'),
      props: true,
    },
    {
      path: '/administracionEmpleados',
      name: 'administraconEmpleados',
      component: () => import('../views/UsuarioAdministrador/EmployeesView.vue'),
    },
    {
      path: '/editarPerfil/:id',
      name: 'editarPerfil',
      component: () => import('../views/UsuarioCliente/EditarPerfilView.vue'),
      props: true,
    },
    {
      path: '/cambiarContraseña/:id',
      name: 'cambiarContraseña',
      component: () => import('../views/UsuarioCliente/ChangePass.vue'),
      props: true,
    },
    {
      path: '/cambiarContraseñaOlvidada/:id',
      name: 'cambiarContraeñaOlvidada',
      component: () => import('../views/UsuarioVisitante/ChangeForgottenPass.vue')
    }
  ],
})

export default router
