<template>
  <v-app>
    <v-main class="bg-light">
      <HandburgerButton class="app-menu-button" @toggle="menuOpen = !menuOpen" />
      <router-view />
      <v-navigation-drawer v-model="menuOpen" temporary location="left">
        <v-list>
          <v-list-item title="Inicio" to="/" />
          <v-list-item title="Inicio de sesión" to="/inicioSesion" />
          <v-list-item title="Sobre Nosotros" />
        </v-list>
      </v-navigation-drawer>
    </v-main>
  </v-app>
</template>

<script setup>
import { ref } from 'vue'

import HandburgerButton from './components/HandburgerButton.vue'

const menuOpen = ref(false)
</script>

<style scoped>
.app-menu-button {
  position: fixed;
  top: 16px;
  left: 16px;
  z-index: 1000;
}
</style>
