<template>
  <v-app>
    <v-main class="bg-light">
      <HamburgerButton class="app-menu-button" @toggle="menuOpen = !menuOpen" />
      <MenuBar v-model="menuOpen" :appMenuIcons="appMenuIcons" />
      <router-view />
      
    </v-main>
  </v-app>
</template>

<script setup>
import { ref } from 'vue'

import HamburgerButton from './components/HamburgerButton.vue'
import MenuBar from './components/MenuBar.vue'

const menuOpen = ref(false)
const appMenuIcons = {
  home: 'mdi-home',
  login: 'mdi-login',
  about: 'mdi-information',
  close: 'mdi-close',
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
