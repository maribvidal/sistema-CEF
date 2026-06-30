<template>
  <v-card rounded="lg">
    <v-card-title class="pa-4 bg-black text-white">Editar Profesor</v-card-title>
    <v-card-text class="pt-4">
      <v-form ref="formEdicion" @submit.prevent="updateEmployee">
        <v-row>
          <v-col cols="12" sm="6" class="py-1">
            <v-text-field
              v-model="employee.nombre"
              label="Nombre"
              variant="outlined"
              density="comfortable"
              required
            ></v-text-field>
          </v-col>
          <v-col cols="12" sm="6" class="py-1">
            <v-text-field
              v-model="employee.apellido"
              label="Apellido"
              variant="outlined"
              density="comfortable"
              required
            ></v-text-field>
          </v-col>
          <v-col cols="12" sm="6" class="py-1">
            <v-text-field
              v-model="employee.nuevo_dni"
              label="DNI"
              variant="outlined"
              density="comfortable"
              prepend-inner-icon="mdi-card-account-details"
              required
            ></v-text-field>
          </v-col>
          <v-col cols="12" sm="6" class="py-1">
            <v-select
              v-model="employee.genero"
              :items="opcionesGenero"
              label="Género"
              variant="outlined"
              density="comfortable"
            ></v-select>
          </v-col>
          <v-col cols="12" sm="6" class="py-1">
            <v-text-field
              v-model="employee.telefono"
              label="Teléfono"
              variant="outlined"
              density="comfortable"
              prepend-inner-icon="mdi-phone"
              required
            ></v-text-field>
          </v-col>
          <v-col cols="12" class="py-1">
            <v-select
              v-model="employee.actividades"
              :items="props.actividades"
              item-title="nombre"
              item-value="id"
              label="Actividades que puede dar"
              multiple
              chips
            ></v-select>
          </v-col>
        </v-row>
      </v-form>
    </v-card-text>
    <v-card-actions class="pa-4">
      <v-spacer></v-spacer>
      <v-btn variant="text" @click="$emit('close')">Cancelar</v-btn>
      <v-btn color="black" variant="elevated" @click="updateEmployee" :loading="loading">Actualizar</v-btn>
    </v-card-actions>
  </v-card>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue'
import { EmployeesService }  from '@/services/EmployeesService' // Asegúrate de tener este servicio para manejar las llamadas a la API
import { ClasesService } from '@/services/ClasesServices'
import { useNotificationStore } from '@/stores/notificationStore.js'

const notificationStore = useNotificationStore()

const props = defineProps({
  empleado: {
    type: Object,
    default: () => ({})
  },
  actividades: {
    type: Array,
    default: () => []
  }
})

const emit = defineEmits(['close', 'updated'])

const opcionesGenero = ['M', 'F', 'O']

const employee = ref({ ...props.empleado })
const loading = ref(false) 

watch(() => props.empleado, (newVal) => {
  employee.value = { 
    ...newVal, 
    nuevo_dni: newVal.dni,
    telefono: newVal.telefono || '' // Si es null/undefined, lo convierte a string vacío
  }
}, { deep: true, immediate: true })

const fetchProfesorActivities = async () => {
  if (!employee.value.id) return
  try {
    const resAct = await ClasesService.listarActividadesProfesor(employee.value.id)
    if (Array.isArray(resAct)) {
      employee.value.actividades = resAct.map(a => a.id ?? a[0])
    }
  } catch (error) {
    console.error("Error fetching professor's activities:", error)
    employee.value.actividades = []
  }
}

onMounted(() => {
  fetchProfesorActivities()
})

const updateEmployee = async () => {
  if (!employee.value.nombre || !employee.value.apellido || !employee.value.nuevo_dni || !employee.value.genero || !employee.value.telefono) {
    notificationStore.showNotification('Por favor, complete todos los campos obligatorios.', 'warning')
    return
  }

  loading.value = true
  try {
    const payload = { ...employee.value }
    await EmployeesService.updateEmployeeInfo(employee.value.dni, payload)

    notificationStore.showNotification('El profesor fue modificado correctamente', 'success')
    emit('updated')
    emit('close')
  } catch (error) {
    console.error('Error al actualizar profesor:', error)
    const statusCode = error.status
    if (statusCode === 409) {
      notificationStore.showNotification('Ya existe un empleado con ese DNI', 'danger')
    } else {
      notificationStore.showNotification('Hubo un error al actualizar los datos.', 'danger')
    }
  } finally {
    loading.value = false
  }
}
</script>
