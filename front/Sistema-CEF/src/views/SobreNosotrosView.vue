<template>
  <v-container class="about-page py-10" fluid>
    <v-row class="justify-center">
      <v-col cols="12" md="10" lg="8">
        <v-card class="about-hero pa-8" elevation="8">
          <div class="eyebrow mb-2">Centro de Entrenamiento Fisico</div>
          <h1 class="text-h3 text-md-h2 mb-4">Nosotros</h1>
          <p class="text-body-1 mb-0">
            Acompañamos a cada persona con un enfoque cercano, profesional y orientado a objetivos reales.
            Nuestro equipo trabaja para que entrenar sea una experiencia clara, segura y sostenible.
          </p>
        </v-card>
      </v-col>
    </v-row>

    <v-row class="justify-center mt-6" dense>
      <v-col cols="12" md="4">
        <v-card class="pa-6 about-card" height="100%">
          <v-card-title class="text-h6 px-0">Nuestra misión</v-card-title>
          <v-card-text class="px-0">
            Crear un espacio accesible donde cada usuario reciba atención real, seguimiento y una propuesta de entrenamiento útil.
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="12" md="4">
        <v-card class="pa-6 about-card" height="100%">
          <v-card-title class="text-h6 px-0">Nuestro equipo</v-card-title>
          <v-card-text class="px-0">
            Profesores, administración y recepción coordinan cada detalle para que la experiencia diaria funcione sin fricción.
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="12" md="4">
        <v-card class="pa-6 about-card" height="100%">
          <v-card-title class="text-h6 px-0">Nuestra propuesta</v-card-title>
          <v-card-text class="px-0">
            Clases, planes de pago y seguimiento en un solo lugar, con una interfaz pensada para consultar y gestionar todo rápido.
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<style scoped>
.about-page {
  min-height: calc(100vh - 120px);
  /* Usa la variable de base.css, con fallback al gradiente si querés, pero para el dark mode es mejor el bg-main */
  background: var(--bg-main, linear-gradient(180deg, #f8fbff 0%, #eef4fb 100%));
}

.about-hero {
  background: var(--bg-card, linear-gradient(135deg, #ffffff 0%, #eef6ff 100%));
  border: 1px solid rgba(25, 118, 210, 0.12);
  color: var(--text-main);
}

.eyebrow {
  letter-spacing: 0.12em;
  text-transform: uppercase;
  font-size: 0.8rem;
  color: var(--primary-color, #1e4f91);
  font-weight: 700;
}

.about-card {
  background-color: var(--bg-card);
  color: var(--text-main);
  border: 1px solid rgba(25, 118, 210, 0.08);
}
</style>