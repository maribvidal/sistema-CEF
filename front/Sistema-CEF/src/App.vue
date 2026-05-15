<template>
  <v-app>
    <v-main class="bg-light">
      
      <NavBar />
      <HamburgerButton class="app-menu-button d-flex d-md-none" @toggle="menuOpen = !menuOpen" />
      <MenuBar v-model="menuOpen" :appMenuIcons="appMenuIcons" />
      
      <router-view />
      
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
}
</script>

<style scoped>




</style>
