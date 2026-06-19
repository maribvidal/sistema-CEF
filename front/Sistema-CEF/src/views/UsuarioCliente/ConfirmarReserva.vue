<template>
    <v-container fluid class="fill-height d-flex align-center justify-center" style="min-height: 100dvh;">
        <v-card class="pa-6 login-card" width="420" elevation="8" color="#f0f0f0" rounded="lg">

            <h1>Confirmar Reserva</h1>
            <p>
                ¿Desea confirmar su reserva para la clase de
                {{ claseSeleccionada?.actividad?.nombre || 'desconocida' }} del día
                {{ claseSeleccionada?.dia || 'desconocido' }}?
            </p>
            <v-btn class="mr-2" color="primary" @click="confirmarReserva">Confirmar</v-btn>
            <v-btn color="red" @click="cancelarReserva">Cancelar</v-btn>
        </v-card>
    </v-container>
</template>

<script setup>
import { useAuth } from '@/services/UsuariosServices.js'
import { useRouter } from 'vue-router'
import { useNotificationStore } from '@/stores/notificationStore.js'
import { ref, computed, onMounted } from 'vue'
import { ClasesService } from '@/services/ClasesServices'

const { userProfile } = useAuth()
const notificationStore = useNotificationStore()
const router = useRouter()

const actividades = ref([
    {
        id: 1,
        nombre: 'Yoga',
        dia: 'desconocido',
    },
    {
        id: 2,
        nombre: 'Pilates',
        dia: 'desconocido',
    },
    {
        id: 3,
        nombre: 'Funcional',
        dia: 'desconocido',
    },
])

const claseSeleccionada = computed(() => actividades.value?.[0] || null)

const obtenerClases = async () => {
    try {
        const responseClases = await ClasesService.listarClases()
        const responseActividades = await ClasesService.listarActividades()
        
        const clasesList = Array.isArray(responseClases) ? responseClases : []
        const actividadesList = Array.isArray(responseActividades) ? responseActividades : []

        actividades.value = clasesList.map(clase => ({
            ...clase,
            actividad: actividadesList.find(a => a.id === clase.actividad_id) || { nombre: 'desconocida' }
        }))
    } catch (error) {
        console.error('Error al obtener información de clases:', error)
        notificationStore.addNotification?.({
            message: 'No se pudo cargar la información de la clase.',
            type: 'error',
        })
    }
}

const confirmarReserva = async () => {
    notificationStore.addNotification?.({
        message: 'Reserva confirmada correctamente.',
        type: 'success',
    })

    await router.push(`/perfil/${userProfile?.id}`)
}

const cancelarReserva = async () => {
    await router.push(`/perfil/${userProfile?.id}`)
}

onMounted(() => {
    obtenerClases()
})

</script>

<style scoped>


</style>