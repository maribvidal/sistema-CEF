<template>
  <v-container class="py-10">
    <v-row justify="center">
      <v-col cols="12" md="8" lg="6">
        <v-card class="pa-6" rounded="lg" elevation="6">
          <v-card-title class="text-h4">You did it!</v-card-title>
          <v-card-subtitle>
            Vuetify ya quedó integrado dentro de Sistema-CEF.
          </v-card-subtitle>

          <v-card-text class="pt-4">
            <p class="mb-4">
              Esta es la pantalla inicial con componentes de Vuetify funcionando en la app
              existente.
            </p>
            <v-btn color="primary" to="/inicioSesion">Ir a inicio de sesión</v-btn>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>