<template>
    <v-app-bar app color="white" elevation="1">
        <!-- Logo Text / Image placeholder -->
        <router-link to="/" class="navbar-logo">
            <v-img class="NavBarIMG" :src="logoImg" alt="Logo CEF" contain height="40" width="150" />
        </router-link>

        <v-spacer></v-spacer>
        <v-btn density="comfortable" rounded="circle" class="theme-btn" color="blue-darken-3" variant="flat">
                <v-icon>mdi-moon-waning-crescent</v-icon>
            </v-btn>
        <!-- Use d-none d-md-flex to hide links on smaller screens if needed -->
        <div class="d-none d-md-flex align-center">
            
            <v-btn variant="text" class="text-none text-subtitle-1 mx-1" color="blue-darken-3" to="/">Inicio</v-btn>
            <v-btn variant="text" class="text-none text-subtitle-1 mx-1" color="blue-darken-3" to="/sobre-nosotros">Nosotros</v-btn>
            <v-btn variant="text" class="text-none text-subtitle-1 mx-1" color="blue-darken-3" to="/clases">Clases</v-btn>
            <!-- Botón de Registro modificado -->
            <v-btn variant="flat" color="blue-darken-3" class="text-none text-subtitle-1 ml-4 mr-2" to="/inicioSesion">
                 <v-icon start>mdi-login</v-icon>
                Iniciar Sesión
            </v-btn>

            <v-btn variant="flat" color="red-darken-2" class="text-none text-subtitle-1 ml-2 mr-2" to="/registro">
                <v-icon start>mdi-account-plus</v-icon>
                Registrarse
            </v-btn>
        </div>
    </v-app-bar>
</template>
<script>
import logoImg from '@/assets/logoLargo.png'

export default {
    name: 'NavBar',
    data() {
        return {
            logoImg,
            appMenuIcons: {
                accountnew: 'mdi-account-plus'
            }
        }
    },
}
</script>

<style scoped>
.navbar-logo {
    display: flex;
    align-items: center;
    text-decoration: none;
    cursor: pointer;
    transition: opacity 0.2s ease;
    margin-left: 10%;
}

@media (max-width: 768px) {
    .navbar-logo {
        margin-left: 15%;
    }

    .theme-btn {
        display: none !important;
    }
}

.navbar-logo:hover {
    opacity: 0.8;
}

.NavBarIMG {
    margin-left: -50px;
    object-fit: contain;
}

.registerButton {
    border: 2px solid black;
    border-radius: 4px;
    padding: 6px 12px;
    transition: background-color 0.3s ease, color 0.3s ease;
}

.registerButton:hover {
    background-color: black;
    color: white;
}

.theme-btn {
    border-radius: 100% !important;
    transition: background-color 0.3s ease, color 0.3s ease;
    max-block-size: 50px;
    max-width: 30px;
    margin-right: 30px;
}
</style>