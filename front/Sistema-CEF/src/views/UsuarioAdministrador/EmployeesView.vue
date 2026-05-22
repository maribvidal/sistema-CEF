<template>
  <v-container class="employees-admin" fluid>
    <v-row justify="center">
      <v-col cols="12" md="10">
        <v-card elevation="2" rounded="lg">
          <v-card-title class="d-flex align-center pa-4 bg-black text-white">
            <v-icon icon="mdi-account-group" class="mr-3"></v-icon>
            <span class="text-h5">Administración de Empleados</span>
            <v-spacer></v-spacer>
            <v-text-field
              v-model="search"
              prepend-inner-icon="mdi-magnify"
              label="Buscar por nombre o DNI"
              variant="solo"
              hide-details
              density="compact"
              class="search-field"
              style="max-width: 300px;"
            ></v-text-field>
          </v-card-title>

          <v-data-table
            :headers="headers"
            :items="empleados"
            :search="search"
            :loading="loading"
            loading-text="Cargando personal..."
            no-data-text="No se encontraron empleados"
          >
            <template v-slot:item.rol_id="{ item }">
              <v-chip :color="getRoleColor(item.rol_id)" size="small" class="font-weight-bold">
                {{ getRoleName(item.rol_id) }}
              </v-chip>
            </template>

            <template v-slot:item.acciones="{ item }">
              <v-btn
                icon="mdi-pencil"
                variant="text"
                color="blue-darken-1"
                @click="abrirEditorRol(item)"
              ></v-btn>
            </template>
          </v-data-table>
        </v-card>
      </v-col>
    </v-row>

    <!-- Diálogo para cambiar Rol -->
    <v-dialog v-model="dialog" max-width="400px">
      <v-card rounded="lg">
        <v-card-title class="bg-grey-lighten-3">Cambiar Rol de Empleado</v-card-title>
        <v-card-text class="pt-4">
          <div class="mb-4">
            <strong>Empleado:</strong> {{ empleadoSeleccionado?.nombre }} {{ empleadoSeleccionado?.apellido }}
          </div>
          <v-select
            v-model="nuevoRolId"
            :items="roles"
            item-title="label"
            item-value="id"
            label="Seleccionar Nuevo Rol"
            variant="outlined"
          ></v-select>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn variant="text" @click="dialog = false">Cancelar</v-btn>
          <v-btn color="black" variant="elevated" @click="confirmarCambioRol">Actualizar</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { EmployeesService } from '@/services/EmployeesService'

const empleados = ref([])
const search = ref('')
const loading = ref(false)
const dialog = ref(false)
const empleadoSeleccionado = ref(null)
const nuevoRolId = ref(null)

const headers = [
  { title: 'DNI', key: 'dni', sortable: true },
  { title: 'Nombre', key: 'nombre' },
  { title: 'Apellido', key: 'apellido' },
  { title: 'Correo', key: 'correo' },
  { title: 'Rol Actual', key: 'rol_id', align: 'center' },
  { title: 'Acciones', key: 'acciones', sortable: false, align: 'end' }
]

const roles = [
  { id: 1, label: 'Administrador' },
  { id: 2, label: 'Recepcionista' },
  { id: 3, label: 'Usuario' }
]

const getRoleName = (id) => roles.find(r => r.id === id)?.label || 'Desconocido'
const getRoleColor = (id) => {
  if (id === 1) return 'red-darken-1'
  if (id === 2) return 'blue-darken-1'
  return 'grey-darken-1'
}

const cargarEmpleados = async () => {
  loading.value = true
  try {
    const data = await EmployeesService.getEmployees()
    // Si el backend devuelve tuplas: 0:id, 1:dni, 2:nombre, 3:apellido, 6:correo, 9:rol_id
    empleados.value = data.map(e => ({
      dni: e.dni ?? e[1],
      nombre: e.nombre ?? e[2],
      apellido: e.apellido ?? e[3],
      correo: e.correo ?? e[6],
      rol_id: e.rol_id ?? e[9]
    }))
  } catch (error) {
    console.error('Error cargando empleados:', error)
  } finally {
    loading.value = false
  }
}

const abrirEditorRol = (empleado) => {
  empleadoSeleccionado.value = empleado
  nuevoRolId.value = empleado.rol_id
  dialog.value = true
}

const confirmarCambioRol = async () => {
  try {
    await EmployeesService.updateEmployeeRole(empleadoSeleccionado.value.dni, nuevoRolId.value)
    await cargarEmpleados()
    dialog.value = false
  } catch (error) {
    alert('Error al actualizar el rol: ' + (error.response?.data?.error || 'Error desconocido'))
  }
}

onMounted(cargarEmpleados)
</script>

<style scoped>
.employees-admin {
  padding-top: 40px;
  background-color: #f5f5f5;
  min-height: 100vh;
}
.search-field :deep(.v-field__input) {
  color: black !important;
}
</style>
