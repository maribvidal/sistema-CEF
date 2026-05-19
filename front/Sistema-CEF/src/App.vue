<template>
  <v-app>
    <v-main class="bg-light">
      
      <NavBar />
      <HamburgerButton class="app-menu-button d-flex d-md-none" @toggle="menuOpen = !menuOpen" />
      <MenuBar v-model="menuOpen" :appMenuIcons="appMenuIcons" />
      
      <router-view />
      

      <v-footer class="pa-4" color="#f0f0f0">
        <span>&copy; 2026 CEF. Todos los derechos reservados.</span>
      </v-footer>
      
    </v-main>
  </v-app>
</template>

<script setup>
import { ref } from 'vue'

import HamburgerButton from './components/HamburgerButton.vue'
import MenuBar from './components/MenuBar.vue'
import NavBar from './components/NavBar.vue'

const menuOpen = ref(false)
const appMenuIcons = {
  home: 'mdi-home',
  login: 'mdi-login',
  about: 'mdi-information',
  close: 'mdi-close',
  gym: 'mdi-dumbbell',
  classes: 'mdi-calendar-blank',
  accountnew: 'mdi-account-plus',
  moon: 'mdi-moon-waning-crescent',
}
</script>

<style scoped>

.v-footer {
  display: flex;
  justify-content: center;
  align-items: center;
}

</style>
