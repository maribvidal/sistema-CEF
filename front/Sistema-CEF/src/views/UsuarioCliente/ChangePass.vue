<template>
    <v-card class="mx-auto" max-width="700" mt-3>
        <v-card-title class="text-h5">Cambiar Contraseña</v-card-title>
        <v-card-text>
      <v-form ref="formChangePass" @submit.prevent="changePassword">
        <v-row>
          <v-col cols="12" sm="6" class="py-1">
            <v-text-field
                id="currentPassword"
              v-model="currentPassword"
              label="Contraseña Actual"
              type="password"
              variant="outlined"
              density="comfortable" 
                required
            ></v-text-field>
          </v-col>
          <v-col cols="12" sm="6" class="py-1">
            <v-text-field
                id="newPassword"
              v-model="newPassword"
              label="Nueva Contraseña"
              type="password"
              variant="outlined"
              density="comfortable"
              required
            ></v-text-field>
          </v-col>
          <v-col cols="12" sm="6" class="py-1">
            <v-text-field
              id="confirmPassword"
              v-model="confirmPassword"
              label="Confirmar Nueva Contraseña"
              type="password"
              variant="outlined"
              density="comfortable"
              required
            ></v-text-field>    
            </v-col>
        </v-row>
        </v-form>
    </v-card-text>
    <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn variant="text" @click="router.back()">Cancelar</v-btn>
        <v-btn color="primary" variant="elevated" @click="changePasswordHandler" :loading="loading">Cambiar Contraseña</v-btn>
    </v-card-actions>

    </v-card>

</template>

<script setup>
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuth } from '@/services/UsuariosServices.js'
import { useNotificationStore } from '@/stores/notificationStore.js'
const router = useRouter()
const route = useRoute()
const { changePassword } = useAuth()
const currentPassword = ref('')
const newPassword = ref('')
const confirmPassword = ref('')
const loading = ref(false)
const notificationStore = useNotificationStore()
/* 400: La nueva contraseña no cumple con las validaciones básicas de longitud o formato
401: Error interno de consulta
402: Usuario no encontrado
403: La contraseña actual es incorrecta
404: La nueva contraseña no puede ser igual a la contraseña actual
500: Error interno al modificar el registro
200: Contraseña modificada exitosamente. */
const changePasswordHandler = async () => {
  if (newPassword.value !== confirmPassword.value) {
    notificationStore.showNotification('Las nuevas contraseñas no coinciden', 'danger')
    return
  }
  loading.value = true
  try {
    const response = await changePassword(route.params.id, {
      currentPassword: currentPassword.value,
      newPassword: newPassword.value
    })
    if(response.status === 400){
      notificationStore.showNotification('La nueva contraseña no cumple con las validaciones básicas de longitud o formato', 'danger')
      return
    }
    if(response.status === 401){
      notificationStore.showNotification('Error interno de consulta', 'danger')
      return
    }
    if(response.status === 402){
      notificationStore.showNotification('Usuario no encontrado', 'danger')
      return
    }
    if(response.status === 403){
      notificationStore.showNotification('La contraseña actual es incorrecta', 'danger')
      return
    }
    if(response.status === 404){
      notificationStore.showNotification('La nueva contraseña no puede ser igual a la contraseña actual', 'danger')
      return
    }
    if(response.status === 500){
      notificationStore.showNotification('Error interno al modificar el registro', 'danger')
      return
    }
    notificationStore.showNotification('Contraseña cambiada exitosamente', 'success')
    router.push(`/perfil/${route.params.id}`)
  } catch (error) {
    console.error('Error al cambiar contraseña:', error)
    notificationStore.showNotification('Error al cambiar contraseña: ' + error.message, 'danger')
  } finally {
    loading.value = false
  }
}

</script>

<style scoped>

</style>