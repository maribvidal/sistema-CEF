<template>
  <v-app>
    <v-main class="bg-light">
      
      <NavBar />
      <HamburgerButton class="app-menu-button d-flex d-md-none" @toggle="menuOpen = !menuOpen" />
      <MenuBar v-model="menuOpen" :appMenuIcons="appMenuIcons" />
      <FloatingNotification />
      <ConfirmNotificacion />

      <router-view />
      

      <v-footer class="pa-4 bg-light">
        <span>&copy; 2026 CEF. Todos los derechos reservados.</span>
      </v-footer>
      
    </v-main>
  </v-app>
</template>

<script setup>
import { RouterLink, RouterView } from 'vue-router'
import { ref, onMounted, watchEffect } from 'vue'
import { useAuth } from '@/services/UsuariosServices.js'

import HamburgerButton from './components/HamburgerButton.vue'
import MenuBar from './components/MenuBar.vue'
import NavBar from './components/NavBar.vue'
import FloatingNotification from './components/FloatingNotificacion.vue'
import ConfirmNotificacion from './components/ConfirmNotificacion.vue'

const menuOpen = ref(false)

const { isLoggedIn, userRole, fetchUserProfile } = useAuth()
const appMenuIcons = {
  home: 'mdi-home',
  login: 'mdi-login',
  about: 'mdi-information',
  close: 'mdi-close',
  gym: 'mdi-dumbbell',
  classes: 'mdi-calendar-blank',
  accountnew: 'mdi-account-plus',
  employees: 'mdi-account-multiple-cog',
  users: 'mdi-account-cog', // <-- Añadir esta línea
  moon: 'mdi-moon-waning-crescent',
  sun: 'mdi-white-balance-sun',
}
onMounted(() => {
  if (isLoggedIn.value) {
    fetchUserProfile()
  }
})
</script>


<style scoped>

.v-footer {
  display: flex;
  justify-content: center;
  align-items: center;
}

</style>
