<template>
    <v-card class="mx-auto" max-width="700" mt-3>
        <v-card-title class="text-h5">Cambiar Contraseña</v-card-title>
        <v-card-text>
      <v-form ref="formChangePass" @submit.prevent="changePassword">
        <v-row>
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
const router = useRouter()
const route = useRoute()
const { changePassword } = useAuth()
const currentPassword = ref('')
const newPassword = ref('')
const confirmPassword = ref('')
const loading = ref(false)
/* 400: La nueva contraseña no cumple con las validaciones básicas de longitud o formato
401: Error interno de consulta
402: Usuario no encontrado
403: La contraseña actual es incorrecta
404: La nueva contraseña no puede ser igual a la contraseña actual
500: Error interno al modificar el registro
200: Contraseña modificada exitosamente. */
const changePasswordHandler = async () => {
  if (newPassword.value !== confirmPassword.value) {
    alert('Las nuevas contraseñas no coinciden')
    return
  }
  loading.value = true
  try {
    const response = await changePassword(route.params.id, {
      currentPassword: currentPassword.value,
      newPassword: newPassword.value
    })
    if(response.status === 400){
      alert('La nueva contraseña no cumple con las validaciones básicas de longitud o formato')
      return
    }
    if(response.status === 401){
      alert('Error interno de consulta')
      return
    }
    if(response.status === 402){
      alert('Usuario no encontrado')
      return
    }
    if(response.status === 403){
      alert('La contraseña actual es incorrecta')
      return
    }
    if(response.status === 404){
      alert('La nueva contraseña no puede ser igual a la contraseña actual')
      return
    }
    if(response.status === 500){
      alert('Error interno al modificar el registro')
      return
    }
    alert('Contraseña cambiada exitosamente')
    router.push(`/perfil/${route.params.id}`)
  } catch (error) {
    console.error('Error al cambiar contraseña:', error)
    alert('Error al cambiar contraseña: ' + error.message)
  } finally {
    loading.value = false
  }
}

</script>

<style scoped>

</style>