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
                  <v-btn color="primary" block @click="goToEdit">Gestionar perfil</v-btn>
                </v-col>
                <v-col cols="12" sm="6">
                  <v-btn color="error" block variant="flat" @click="goToChangePassword">Cambiar contraseña</v-btn>
                </v-col>
                <v-col cols="12" sm="6">
                  <v-btn color="secondary" block variant="flat" @click="handleGenerateQR">Generar QR</v-btn>
                </v-col>
              </v-row>
            </v-col>
          </v-row>
        </v-card>
      </v-col>
    </v-row>
    <v-dialog v-model="dialogQR" max-width="400px">
      <v-card>
        <v-card-title class="text-h5">Código QR</v-card-title>
        <v-card-text>
          <div class="d-flex justify-center">
            <v-img :src="qrSrc" alt="QR Code" max-width="300" />
          </div>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn text @click="dialogQR = false">Cerrar</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuth } from '@/services/UsuariosServices.js'
import DateFormatterService from '@/services/DateFormatterService.js'
// 1. Importamos la nueva función unificada
import { getValidImageSrc } from '@/services/ImageFormatterService.js' 
import defaultLogo from '@/assets/logoLargo.png'
import UsuariosService from '@/services/UsuariosServices.js'

const router = useRouter()
const route = useRoute()
const { logout, fetchUserProfileById, userProfile: currentUser } = useAuth()
const { formatSpanishDate } = DateFormatterService

const profileData = ref(null)
// 2. avatarSrc ahora es un ref, inicializado con el logo por defecto
const avatarSrc = ref(defaultLogo) 

const getProfile = async () => {
  try {
    const profile = await fetchUserProfileById(route.params.id)
    profileData.value = profile
    
    // 3. Procesamos la imagen de forma asíncrona usando nuestro servicio inteligente
    if (profile?.avatarUrl) {
      const srcProcessado = await getValidImageSrc(profile.avatarUrl)
      if (srcProcessado) avatarSrc.value = srcProcessado
    }
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
      case 2: return 'Recepcionista'
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
const userBirthDate = computed(() => formatSpanishDate(profileData.value?.fecha_nac))

const isOwnProfile = computed(() => currentUser.value?.id == route.params.id)

const onLogout = async () => {
  await logout()
  router.push('/inicioSesion')
}

const goToEdit = () => {
  router.push(`/editarPerfil/${route.params.id}`)
}

const goToChangePassword = () => {
  router.push(`/cambiarContraseña/${route.params.id}`)
}

const dialogQR = ref(false)
const qrSrc = ref(null)

// 1. Renombramos la función local (ej: handleGenerateQR o downloadQR)


const handleGenerateQR = async () => {
  try {
    
    const resultado = await UsuariosService.generarQR(route.params.id) 
    
    dialogQR.value = true

    
    if (resultado instanceof Blob) {
      
      const url = URL.createObjectURL(resultado)
      qrSrc.value = url
      
      setTimeout(() => URL.revokeObjectURL(url), 1000)
      
    } else if (resultado && typeof resultado === 'string') {
      
      console.log('Recibimos un string. Intentando abrir...')
      window.open(resultado, '_blank')
      
    } else if (resultado && typeof resultado === 'object') {
      
      console.log('Recibimos un JSON. Revisa las propiedades del objeto arriba.')
      
    } else {
      console.error('El formato recibido no es reconocido y no se puede crear el QR.')
    }

  } catch (error) {
    console.error('Error al generar el QR:', error)
  }
}
</script>

<style scoped>
.text-h5 {
  font-weight: 600;
}
.text--secondary {
  color: var(--text-secondary);
}
</style>