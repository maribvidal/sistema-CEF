<template>
    <v-app-bar app color="white" elevation="1">
        <!-- Logo Text / Image placeholder -->
        <v-img class="NavBarIMG" :src="logoImg" alt="Logo CEF" contain height="40"/>

        <v-spacer></v-spacer>

        <!-- Use d-none d-md-flex to hide links on smaller screens if needed -->
        <div class="d-none d-md-flex align-center">
            <v-btn variant="text" class="text-none text-subtitle-1 mx-1" color="black" to="/">Inicio</v-btn>
            <v-btn variant="text" class="text-none text-subtitle-1 mx-1" color="black" to="/inicioSesion">Iniciar Sesión</v-btn>
            <v-btn variant="text" class="text-none text-subtitle-1 mx-1" color="black" to="/sobre-nosotros">Nosotros</v-btn>
            
            <!-- Botón de Registro modificado -->
            <v-btn variant="flat" color="red" class="text-none text-subtitle-1 ml-4 mr-2" to="/registro">Registrarse</v-btn>
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
.registerButton {
    border: 2px solid black;
    border-radius: 4px;
    padding: 6px 12px;
    transition: background-color 0.3s ease, color 0.3s ease;

}
</style>