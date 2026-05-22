<template>
    <v-container class="home-view" fluid>
        <v-container class="slideshow-container" fluid>

        <SlideShow />
        
        </v-container>

        <v-card-text class="elige-planes">
        <h2 class="text-center mb-4">Elige tu forma de pago</h2>
        <v-row class="justify-center">
          <v-col cols="12" md="4">
            <v-card class="pa-4" color="#f0f0f0">
              <v-card-title class="text-h6">Por Clase</v-card-title>
              <v-card-text>
                Acceso a las instalaciones en horarios específicos.
                <ul>
                  <li>Acceso limitado a ciertas áreas.</li>
                  <li>Sin clases grupales.</li>
                </ul>
              </v-card-text>
              <v-card-actions>
                <v-btn block color="red" size="large" :to="'/clases'">Seleccionar</v-btn>
              </v-card-actions>
            </v-card>
          </v-col>
          <v-col cols="12" md="4">
            <v-card class="pa-4" color="#f0f0f0">
              <v-card-title class="text-h6">Mensual</v-card-title>
              <v-card-text>
                Acceso completo a las instalaciones durante todo el horario de apertura.
                <ul>
                  <li>Acceso a todas las áreas.</li>
                  <li>Incluye clases grupales ilimitadas.</li>
                </ul>
              </v-card-text>
              <v-card-actions>
                <v-btn block color="red" size="large">Seleccionar</v-btn>
              </v-card-actions>
            </v-card>
          </v-col>
        </v-row>
      </v-card-text>
    </v-container>
</template>

<script setup>
import SlideShow from '@/components/SlideShow.vue'
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