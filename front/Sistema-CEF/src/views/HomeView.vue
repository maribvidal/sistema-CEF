<template>
    <v-container class="home-view" fluid>
        <v-container class="slideshow-container" fluid>

        <SlideShow />
        
        </v-container>

        <v-card-text class="elige-planes" v-if="userRole === 3">
        <h2 class="text-center mb-4">¿Quieres accceder a nuestras clases?</h2>
        <v-row class="justify-center">
          <v-col cols="12" md="4" sm="6" class="mb-4">
            <v-card class="pa-4" color="--bg-card">
              <v-card-title class="text-h6">Elige tu clase</v-card-title>
              <v-card-text>
                
                <ul>
                  <li>Acceso a todas las clases grupales.</li>
                  <li>Paga tus clases de forma mensual o individual.</li>
                </ul>
              </v-card-text>
              <v-card-actions>
                <v-btn block color="red" size="large" :to="'/clases'">Ir a nuestras clases</v-btn>
              </v-card-actions>
            </v-card>
          </v-col>
          
        </v-row>
      </v-card-text>
    </v-container>
</template>

<script setup>
import SlideShow from '@/components/SlideShow.vue'
import { useAuth } from '@/services/UsuariosServices.js'

const { userRole } = useAuth()
</script>

<style scoped>
.home-view {
  
}
.slideshow-container {
    position: inherit;
    display: flex;
    justify-content: center;
    align-items: center;
    width: 100%;
    height: 100%;
}
</style>