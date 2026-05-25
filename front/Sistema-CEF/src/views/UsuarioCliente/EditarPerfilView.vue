<template>
  <v-container class="mt-5">
    <v-row justify="center">
      <v-col cols="12" md="8">
        <v-card class="pa-4">
          <v-card-title class="text-h5">Editar perfil</v-card-title>
          <v-card-text>
            <v-form @submit.prevent="updateProfile">
              <div class="d-flex justify-center mb-4">
                <AvatarInput :current-avatar="avatarSrc" @image-cropped="handleAvatarCropped" />
              </div>
              <v-text-field v-model="userName" label="Nombre" variant="outlined" />
              <v-text-field v-model="lastName" label="Apellido" variant="outlined" />
              <v-text-field v-model="userEmail" label="Correo electrónico" variant="outlined" />
              <v-text-field v-model="userPhone" label="Teléfono" variant="outlined" />
              <v-text-field v-model="userBirthDate" label="Fecha de nacimiento" type="date" variant="outlined" />
              <v-btn type="submit" color="primary" class="mt-4" :loading="isUpdatingProfile" :disabled="isUpdatingProfile">Guardar cambios</v-btn>
              <v-btn color="error" variant="flat" class="mt-4 ml-2" :to="`/perfil/${routerParamsId}`">Cancelar</v-btn>
            </v-form>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref, onMounted, computed, watch, onBeforeUnmount } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuth } from '@/services/UsuariosServices.js'
import DateFormatterService from '@/services/DateFormatterService.js'
import AvatarInput from '@/components/AvatarInput.vue'
// 1. Importamos nuestra función principal unificada
import { getValidImageSrc } from '@/services/ImageFormatterService.js'

const router = useRouter()
const route = useRoute()
const { fetchUserProfileById, userProfile, fetchUserProfile, updateProfile: authUpdateProfile, uploadAvatar: authUploadAvatar } = useAuth()
const { formatDateForBackend } = DateFormatterService

const profileData = ref(null)
const getProfile = async () => {
  try {
    const profile = await fetchUserProfileById(route.params.id)
    profileData.value = profile
  } catch (error) {
    console.error('Error fetching profile:', error)
  }
}
const newImage = ref(null)
const isUpdatingProfile = ref(false)
const isUploadingAvatar = ref(false)
const localAvatarPreviewUrl = ref(null)

const routerParamsId = computed(() => route.params.id)
const userName = ref('')
const lastName = ref('')
const userEmail = ref('')
const userBirthDate = ref('')
const userPhone = ref('')
const defaultLogo = '/path/to/default-logo.png' // Ajustar según tu app
const avatarSrc = ref(defaultLogo)

onMounted(() => {
  getProfile()
})

// 2. Convertimos el watch en asíncrono para procesar la imagen del backend
watch(profileData, async (newData) => {
  if (newData) {
    userName.value = newData.nombre || ''
    lastName.value = newData.apellido || ''
    userEmail.value = newData.correo || ''
    userPhone.value = newData.telefono || ''
    userBirthDate.value = formatDateForBackend(newData.fecha_nac) || ''
    
    // Si viene una imagen del backend, la pasamos por el servicio
    if (newData.avatarUrl) {
      const srcProcesado = await getValidImageSrc(newData.avatarUrl)
      avatarSrc.value = srcProcesado || localAvatarPreviewUrl.value || defaultLogo
    } else {
      avatarSrc.value = localAvatarPreviewUrl.value || defaultLogo
    }
  }
}, { immediate: true })

const revokeLocalAvatarPreview = () => {
  if (localAvatarPreviewUrl.value) {
    URL.revokeObjectURL(localAvatarPreviewUrl.value)
    localAvatarPreviewUrl.value = null
  }
}

const handleUploaded = (resp) => {
  avatarSrc.value = resp.url || resp.avatarUrl || resp.data.url
}

const updateProfile = async () => {
  if (!profileData.value) return
  isUpdatingProfile.value = true
  try {
    await authUpdateProfile({
      nombre: userName.value,
      apellido: lastName.value,
      correo: userEmail.value,
      telefono: userPhone.value,
      fecha_nac: userBirthDate.value
    })
    router.push(`/perfil/${routerParamsId.value}`)
  } catch (error) {
    console.error('Error updating profile:', error)
  } finally {
    isUpdatingProfile.value = false
  }
}

const handleAvatarCropped = async (file) => {
  revokeLocalAvatarPreview()
  localAvatarPreviewUrl.value = URL.createObjectURL(file)
  avatarSrc.value = localAvatarPreviewUrl.value
  newImage.value = file
  await uploadAvatar()
}

const uploadAvatar = async () => {
  if (!userProfile.value?.id || !newImage.value) {
    alert('Por favor, selecciona un archivo de imagen.')
    return
  }
  isUploadingAvatar.value = true

  const toBase64 = (file) =>
    new Promise((resolve, reject) => {
      const reader = new FileReader()
      reader.readAsDataURL(file)
      reader.onload = () => resolve(reader.result.split(',')[1]) // Extrae solo datos puros para el backend
      reader.onerror = (error) => reject(error)
    })

  try {
    const base64String = await toBase64(newImage.value)
    const avatarData = {
      base64: base64String,
      nombre: newImage.value.name,
    }
    
    await authUploadAvatar(avatarData)
    await fetchUserProfile(true) 
    await getProfile() 
    
    const updatedProfile = await fetchUserProfileById(route.params.id)
    
    // 3. Pasamos por el validador el avatar actualizado
    if (updatedProfile?.avatarUrl) {
      const updatedSrc = await getValidImageSrc(updatedProfile.avatarUrl)
      avatarSrc.value = updatedSrc || localAvatarPreviewUrl.value || defaultLogo
    } else {
      avatarSrc.value = localAvatarPreviewUrl.value || defaultLogo
    }

  } catch (error) {
    if(error.response && error.response.status === 401) {
      router.push('/inicioSesion')
      return
    }
    console.error('Error al actualizar el avatar:', error)
  } finally {
    isUploadingAvatar.value = false
  }
}

onBeforeUnmount(() => {
  revokeLocalAvatarPreview()
})
</script>

<style scoped>
</style>