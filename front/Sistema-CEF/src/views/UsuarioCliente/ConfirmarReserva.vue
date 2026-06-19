<template>
    <v-container fluid class="fill-height d-flex align-center justify-center" style="min-height: 100dvh;">
        <v-card class="pa-6 login-card" width="420" elevation="8" color="#f0f0f0" rounded="lg">

            <h1 >Confirmar Reserva</h1>
            <p>¿Desea confirmar su reserva para la clase de {{ actividades[0]?.nombre || 'desconocida' }} del dia {{ $clasesInfo.dia || 'desconocida' }}?</p>
            <v-btn color="primary" @click="confirmarReserva">Confirmar</v-btn>
            <v-btn color="red" @click="$router.push(`/perfil/${userProfile?.id}`)">Cancelar</v-btn>
        </v-card>
    </v-container>
</template>

<script setup>
import { useAuth } from '@/services/UsuariosServices.js'
import { useRouter } from 'vue-router'
import { useNotificationStore } from '@/stores/notificationStore.js'
import { ref } from 'vue'
import { ClasesService } from '@/services/ClasesServices'

const { userProfile } = useAuth()
const notificationStore = useNotificationStore()
const router = useRouter()

const actividades = ref([
    { id: 1,
      nombre: 'Yoga',
    },
    { id: 2,
      nombre: 'Pilates',
    },
    { id: 3,
      nombre: 'Funcional',
    },
])

const clasesInfo = async () => {
    try {
        const response = await ClasesService.listarClases()
        actividades.value = response.data
    } catch (error) {
        console.error('Error al obtener información de clases:', error)
    }
}

</script>

<style scoped>


</style>