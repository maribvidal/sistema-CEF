<template>

    <v-container class="mt-5">
    <v-row justify="center">
      <v-col cols="12" md="8">
        <v-card class="pa-4">
          <v-card-title class="text-h5">Editar perfil</v-card-title>
          <v-card-text>
            <v-form @submit.prevent="updateProfile">
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

import { ref, onMounted, computed, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuth } from '@/services/UsuariosServices.js'
import DateFormatterService from '@/services/DateFormatterService.js'
import AvatarCropper from 'vue-avatar-cropper'


const router = useRouter()
const route = useRoute()
const { fetchUserProfileById, userProfile, updateProfile: authUpdateProfile, uploadAvatar: authUploadAvatar } = useAuth()
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

onMounted(() => {
  getProfile()
})

watch(profileData, (newData) => {
  if (newData) {
    userName.value = newData.nombre || ''
    lastName.value = newData.apellido || ''
    userEmail.value = newData.correo || ''
    userPhone.value = newData.telefono || ''
    userBirthDate.value = formatDateForBackend(newData.fecha_nac) || ''
  }
}, { immediate: true })

const routerParamsId = computed(() => route.params.id)
const userName = ref('')
const lastName = ref('')
const userEmail = ref('')
//const userRole = computed(() => profileData.value?.rol_id || profileData.value?.tipo || 'Visitante')
const userBirthDate = ref('')
const userPhone = ref('')
const defaultLogo = '/path/to/default-logo.png' // Adjust this as needed
const avatarSrc = ref(defaultLogo)


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
  isUploadingAvatar.value = true
  try {
    await authUploadAvatar(profileData.value.id, file)
    // Refetch profile to get updated avatar URL
    await getProfile()
  } catch (error) {
    console.error('Error uploading avatar:', error)
  } finally {
    isUploadingAvatar.value = false
  }
}

</script>

<style scoped>

</style>
