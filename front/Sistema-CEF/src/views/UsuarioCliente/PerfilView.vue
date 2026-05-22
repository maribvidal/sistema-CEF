<template>
  <v-container class="pa-6">
    <v-row justify="center">
      <v-col cols="12" md="8">
        <v-card elevation="6" class="pa-4">
          <v-row>
            <v-col cols="12" md="4" class="d-flex justify-center align-center">
              <v-avatar size="120">
                <v-img :src="avatarSrc" alt="Avatar" />
              </v-avatar>
            </v-col>

            <v-col cols="12" md="8">

              <div class="text-h5">{{ userName }} {{ lastName }}</div>
              <div class="text-subtitle-1 text--secondary">{{ userEmail }}</div>
              <div class="text-subtitle-1 text--secondary">Fecha de nacimiento: <strong>{{ userBirthDate }}</strong></div>
              <div class="mt-3">Rol: <strong>{{ rolUser }}</strong></div>

              <v-row class="mt-6" align="center" v-if="isOwnProfile">
                <v-col cols="12" sm="6">
                  <v-btn color="primary" block @click="goToEdit">Editar perfil</v-btn>
                </v-col>
                <v-col cols="12" sm="6">
                  <v-btn color="error" block variant="flat" @click="onLogout">Cerrar sesión</v-btn>
                </v-col>
              </v-row>
            </v-col>
          </v-row>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuth } from '@/services/UsuariosServices.js'
import defaultLogo from '@/assets/logoLargo.png'
import DateFormatterService from '@/services/DateFormatterService.js'

const router = useRouter()
const route = useRoute()
const { logout, fetchUserProfileById, userProfile: currentUser } = useAuth()
const { formatSpanishDate } = DateFormatterService

const profileData = ref(null)

const getProfile = async () => {
  try {
    const profile = await fetchUserProfileById(route.params.id)
    profileData.value = profile
  } catch (error) {
    console.error('Error fetching profile:', error)
  }
}

onMounted(() => {
  getProfile()
})

const rolUser = computed(() => {
  if(profileData.value?.rol_id) {
    switch(profileData.value.rol_id) {
      case 1: return 'Administrador'
      case 2: return 'Gerente'
      case 3: return 'Cliente'
      default: return 'Desconocido'
    }
  } else {
    return profileData.value?.tipo || 'Visitante'
  }
})

const userName = computed(() => profileData.value?.nombre || 'Usuario')
const lastName = computed(() => profileData.value?.apellido || '')
const userEmail = computed(() => profileData.value?.correo || '')
//const userRole = computed(() => profileData.value?.rol_id || profileData.value?.tipo || 'Visitante')
const userBirthDate = computed(() => formatSpanishDate(profileData.value?.fecha_nac))
const avatarSrc = computed(() => profileData.value?.avatarUrl || defaultLogo)

// Mostrar botones solo si el perfil que estamos viendo es el nuestro
const isOwnProfile = computed(() => currentUser.value?.id == route.params.id)

const onLogout = async () => {
  await logout()
  router.push('/inicioSesion')
}

const goToEdit = () => {
  // Ruta de ejemplo; modificar según rutas reales de la app
  router.push('/editar-perfil')
}
</script>

<style scoped>
.text-h5 {
  font-weight: 600;
}
.text--secondary {
  color: rgba(0,0,0,0.6);
}
</style>
