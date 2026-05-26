<template>
  <v-card rounded="lg">
    <v-card-title class="pa-4 bg-black text-white">Editar Empleado</v-card-title>
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
          <v-col cols="12" class="py-1">
            <v-text-field
              v-model="employee.correo"
              label="Correo Electrónico"
              variant="outlined"
              density="comfortable"
              prepend-inner-icon="mdi-email"
              required
            ></v-text-field>
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
import { ref, watch } from 'vue'
import { EmployeesService }  from '@/services/EmployeesService' // Asegúrate de tener este servicio para manejar las llamadas a la API
const props = defineProps({
  empleado: {
    type: Object,
    default: () => ({})
  }
})

const emit = defineEmits(['close', 'updated'])

const employee = ref({ ...props.empleado })
const loading = ref(false)

watch(() => props.empleado, (newVal) => {
  employee.value = { ...newVal }
}, { deep: true, immediate: true })

const updateEmployee = async () => {
  if (!employee.value.nombre || !employee.value.apellido || !employee.value.correo) {
    alert('Por favor, complete todos los campos obligatorios.')
    return
  }

  loading.value = true
  try {
    // Cuando integrés tu API puedes llamar a:
    await EmployeesService.updateEmployeeInfo(employee.value.id, employee.value)
    
    alert('Empleado actualizado exitosamente')
    emit('updated')
    emit('close')
  } catch (error) {
    console.error('Error al actualizar empleado:', error)
    alert('Hubo un error al actualizar los datos.')
  } finally {
    loading.value = false
  }
}
</script>
