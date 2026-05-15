<template>
  <v-container class="classes-view" fluid>
    <v-row justify="center">
      <v-col cols="12" md="10">
        <h1 class="text-h4 mb-6 text-center font-weight-bold">Nuestras Clases</h1>
        
        <v-row>
          <v-col 
            v-for="clase in clasesMock" 
            :key="clase.id" 
            cols="12" 
            sm="6" 
            lg="4"
          >
            <v-card class="class-card" elevation="0">
              <v-img
                :src="clase.imagen"
                height="200px"
                cover
                class="align-end"
              >
                <v-card-title class="text-white bg-black-overlay text-uppercase font-weight-black">
                  {{ clase.categoria }}
                </v-card-title>
              </v-img>

              <v-card-text class="pt-4">
                <div class="d-flex align-center mb-2">
                  <v-icon size="small" class="mr-2" color="primary">mdi-account-tie</v-icon>
                  <span class="text-body-2 font-weight-bold">Profesor:</span>
                  <span class="text-body-2 ml-1">{{ clase.profesor }}</span>
                </div>

                <div class="d-flex align-center mb-2">
                  <v-icon size="small" class="mr-2" color="primary">mdi-calendar-range</v-icon>
                  <span class="text-body-2 font-weight-bold">Día:</span>
                  <span class="text-body-2 ml-1">{{ clase.dia }}</span>
                </div>

                <div class="d-flex align-center mb-2">
                  <v-icon size="small" class="mr-2" color="primary">mdi-clock-outline</v-icon>
                  <span class="text-body-2 font-weight-bold">Hora:</span>
                  <span class="text-body-2 ml-1">{{ clase.hora }}</span>
                </div>

                <div class="d-flex align-center mb-2">
                  <v-icon size="small" class="mr-2" color="primary">mdi-map-marker-outline</v-icon>
                  <span class="text-body-2 font-weight-bold">Sala:</span>
                  <span class="text-body-2 ml-1">{{ clase.sala }}</span>
                </div>
              </v-card-text>

              <v-divider class="mx-4"></v-divider>

              <v-card-actions class="pa-4">
                <v-btn
                  color="black"
                  variant="elevated"
                  block
                  rounded="pill"
                >
                  Ver más información
                </v-btn>
              </v-card-actions>
            </v-card>
          </v-col>
        </v-row>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref } from 'vue'

// Datos de prueba (Mock data) para el diseño
const clasesMock = ref([
  {
    id: 1,
    categoria: 'Funcional',
    profesor: 'Lucas Gómez',
    dia: 'Lunes',
    hora: '08:00',
    sala: 'Sala 1',
    imagen: 'https://images.unsplash.com/photo-1534438327276-14e5300c3a48?q=80&w=500'
  },
  {
    id: 2,
    categoria: 'Yoga',
    profesor: 'Elena Paz',
    dia: 'Martes',
    hora: '10:00',
    sala: 'Sala 2',
    imagen: 'https://images.unsplash.com/photo-1544367567-0f2fcb009e0b?q=80&w=500'
  },
  {
    id: 3,
    categoria: 'Pilates',
    profesor: 'Marcos Rueda',
    dia: 'Miércoles',
    hora: '19:00',
    sala: 'Sala 3',
    imagen: 'https://images.unsplash.com/photo-1534258936925-c58bed479fcb?q=80&w=500'
  }
  ])
</script>

<style scoped>
.classes-view {
  padding-top: 40px;
  background-color: #f5f5f5; /* Fondo gris claro para que resalten las cards blancas */
  min-height: 100vh;
}

.class-card {
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05) !important;
  transition: transform 0.3s ease;
}

.class-card:hover {
  transform: translateY(-5px);
}

.bg-black-overlay {
  background: rgba(0, 0, 0, 0.4);
  width: 100%;
}
</style>