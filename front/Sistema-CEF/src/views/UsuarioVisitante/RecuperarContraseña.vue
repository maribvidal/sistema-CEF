<template>
    <v-container class="fill-height d-flex flex-column align-center justify-center" >
        <v-card class="pa-4" width="400" color="#f0f0f0">
            <v-card-title class="text-h5">Recuperar contraseña</v-card-title>
            <v-card-subtitle>Ingresa tu correo electrónico para recibir instrucciones</v-card-subtitle>

            <v-card-text class="pt-4">
                <v-form>
                    <v-text-field label="Correo electrónico" prepend-inner-icon="mdi-email" variant="outlined" />
                    <v-btn block color="red" size="large" class="mt-2">Enviar instrucciones</v-btn>
                </v-form>
            </v-card-text>
            <v-card-text class="pt-0 mt-2" align="center">
                <v-btn to="/inicioSesion" variant="flat" color="primary" size="small">
                    Volver al inicio de sesión
                </v-btn>
            </v-card-text>
        </v-card>
    </v-container>
</template>

<script>


</script>

<style scoped>

</style>
