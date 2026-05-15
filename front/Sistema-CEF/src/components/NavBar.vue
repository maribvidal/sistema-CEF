<template>
    <v-app-bar app color="white" elevation="1">
        <!-- Logo Text / Image placeholder -->
        <v-img class="NavBarIMG" :src="logoImg" alt="Logo CEF" contain height="40" />

        <v-spacer></v-spacer>

        <!-- Use d-none d-md-flex to hide links on smaller screens if needed -->
        <div class="d-none d-md-flex align-center">
            <v-btn variant="text" class="text-none text-subtitle-1 mx-1" color="black" to="/">Inicio</v-btn>
            <v-btn variant="text" class="text-none text-subtitle-1 mx-1" color="black" to="/inicioSesion">Iniciar Sesión</v-btn>
            <v-btn variant="text" class="text-none text-subtitle-1 mx-1" color="black" to="/sobre-nosotros">Nosotros</v-btn>
        </div>
    </v-app-bar>
</template>
<script>
import logoImg from '@/assets/logoLargo.png'

export default {
    name: 'NavBar',
    data() {
        return {
            logoImg
        }
    },
}
</script>

<style scoped>
.NavBarIMG{
    margin-left: -50px;
}
</style>