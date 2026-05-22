<template>
    <v-container class="mt-5">
    <v-row justify="center">
      <v-col cols="12" md="8">
        <v-card class="pa-4">
          <v-card-title class="text-h5">Editar perfil</v-card-title>
          <v-card-text>
            <v-form @submit.prevent="saveChanges">
              <v-text-field v-model="userName" label="Nombre" variant="outlined" />
              <v-text-field v-model="lastName" label="Apellido" variant="outlined" />
              <v-text-field v-model="userEmail" label="Correo electrónico" variant="outlined" />
              <v-text-field v-model="userBirthDate" label="Fecha de nacimiento" type="date" variant="outlined" />
              <v-btn type="submit" color="primary" class="mt-4">Guardar cambios</v-btn>
                <v-btn color="error" variant="flat" class="mt-4 ml-2" @click="cancelEdit" :to="`/perfil/${routerParamsId}`">Cancelar</v-btn>
            </v-form>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuth } from '@/services/UsuariosServices.js'
import DateFormatterService from '@/services/DateFormatterService.js'

const router = useRouter()
const route = useRoute()
const { fetchUserProfileById, userProfile } = useAuth()
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

const routerParamsId = computed(() => route.params.id)
const userName = computed(() => profileData.value?.nombre || 'Usuario')
const lastName = computed(() => profileData.value?.apellido || '')
const userEmail = computed(() => profileData.value?.correo || '')
//const userRole = computed(() => profileData.value?.rol_id || profileData.value?.tipo || 'Visitante')
const userBirthDate = computed(() => formatSpanishDate(profileData.value?.fecha_nac))
const avatarSrc = computed(() => profileData.value?.avatarUrl || defaultLogo)

</script>

<style scoped>
</style>
