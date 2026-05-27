<template>
    <v-container class="fill-height d-flex flex-column align-center justify-center" @submit.prevent="restorePassButton" >
        <v-card class="pa-4" width="400" color="#f0f0f0">
            <v-card-title class="text-h5">Recuperar contraseña</v-card-title>
            <v-card-subtitle>Ingresa tu correo electrónico para recibir instrucciones</v-card-subtitle>

            <v-card-text class="pt-4">
                <v-form>
                    <v-text-field label="Correo electrónico" prepend-inner-icon="mdi-email" variant="outlined" v-model="userEmail"/>
                    <v-btn @click="restorePassButton" block color="red" size="large" class="mt-2" >Recuperar Contraseña</v-btn>
                </v-form>
            </v-card-text>
            <v-card-text class="pt-0 mt-2" align="center">
                <v-btn to="/inicioSesion" variant="flat" color="primary" size="small">
                    Volver al inicio de sesión
                </v-btn>
            </v-card-text>
        </v-card>
    </v-container>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuth } from '@/services/UsuariosServices.js'
import { useNotificationStore } from '@/stores/notificationStore.js'
const router = useRouter()
const route = useRoute()
const { restorePassword } = useAuth()
const userEmail = ref('')
const notificationStore = useNotificationStore()

const restorePassButton = async () => {
    if(userEmail.value === ''){
        notificationStore.showNotification('Por favor, ingresa tu correo electrónico', 'warning')
        return
    }
    try{
        const response = await restorePassword(userEmail.value)
        if(response && response.status === 200){
            notificationStore.showNotification('Se han enviado las instrucciones a tu correo electrónico', 'success')
            router.push('/inicioSesion')
        } else {
            notificationStore.showNotification('Error al enviar las instrucciones, por favor intenta nuevamente', 'danger')
        }
    }
    catch(error){
        notificationStore.showNotification('Error al enviar las instrucciones ', 'danger')
    }
}
</script>

<style scoped>

</style>
