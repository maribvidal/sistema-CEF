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
            <v-btn variant="text" class="text-none text-subtitle-1 mx-1" color="blue-darken-3" to="/administracionEmpleados">Administracion de empleados</v-btn>
            <!-- Botón de Registro modificado -->
            <v-btn variant="flat" color="blue-darken-3" class="text-none text-subtitle-1 ml-4 mr-2" to="/inicioSesion" v-if="!isLoggedIn">
                 <v-icon start>mdi-login</v-icon>
                Iniciar Sesión
            </v-btn>

            <v-btn variant="flat" color="red-darken-2" class="text-none text-subtitle-1 ml-2 mr-2" to="/registro" v-if="!isLoggedIn">
                <v-icon start>mdi-account-plus</v-icon>
                Registrarse
            </v-btn>
            <!-- Mostrar nombre de usuario si está autenticado -->
            <v-btn variant="text" class="text-none text-subtitle-1 mx-1" color="blue-darken-3" :to="{ name: 'perfil', params: { id: userProfile?.id } }" v-if="isLoggedIn">
                <v-avatar size="32" class="mr-2" v-if="userProfile?.avatarUrl">
                    <v-img :src="userProfile?.avatarUrl" alt="Foto de perfil" cover></v-img>
                </v-avatar>
                <v-icon size="32" class="mr-2" v-else>mdi-account-circle</v-icon>
                Mi Perfil: {{ userProfile?.nombre || 'Usuario' }}
            </v-btn>
            <!-- Botón de logout si está autenticado -->
            <v-btn variant="flat" color="red-darken-2" class="text-none text-subtitle-1 ml-2 mr-2" @click="handleLogout" v-if="isLoggedIn">
                <v-icon start>mdi-logout</v-icon>
                Cerrar Sesión
            </v-btn>

            
            
        </div>
    </v-app-bar>
</template>

<script setup>
import logoImg from '@/assets/logoLargo.png'
import { useAuth } from '@/services/UsuariosServices.js'
import { useRouter } from 'vue-router'

const router = useRouter()
const { isLoggedIn, userProfile, logout } = useAuth()

const handleLogout = async () => {
    await logout()
    router.push('/inicioSesion')
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