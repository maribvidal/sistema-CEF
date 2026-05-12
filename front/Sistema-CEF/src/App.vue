<template>
  <v-app>
    <v-main class="bg-light">
      <HandburgerButton class="app-menu-button" @toggle="menuOpen = !menuOpen" />
      <NavBar v-model="menuOpen" :appMenuIcons="appMenuIcons" />
      <router-view />
      
    </v-main>
  </v-app>
</template>

<script setup>
import { ref } from 'vue'

import HandburgerButton from './components/HandburgerButton.vue'
import NavBar from './components/NavBar.vue'

const menuOpen = ref(false)
const appMenuIcons = {
  home: 'mdi-home',
  login: 'mdi-login',
  about: 'mdi-information',
}
</script>

<style scoped>
.app-menu-button {
  position: fixed;
  top: 16px;
  left: 16px;
  z-index: 1000;
}
</style>
