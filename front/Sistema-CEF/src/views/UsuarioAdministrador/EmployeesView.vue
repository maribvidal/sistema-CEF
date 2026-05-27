<template>
  <v-container class="employees-admin" fluid>
    <v-row justify="center">
      <v-col cols="12" md="10">
        <v-card elevation="2" rounded="lg">
          <v-card-title class="d-flex align-center pa-4 bg-black text-white">
            <v-icon icon="mdi-account-group" class="mr-3"></v-icon>
            <span class="text-h5">Administración de Empleados</span>
            <v-spacer></v-spacer>
            <v-btn
              color="white"
              variant="outlined"
              prepend-icon="mdi-account-tie"
              class="mr-2 text-none"
              density="comfortable"
              @click="crearProfesor"
            >
              Crear Profesor
            </v-btn>
            <v-btn
              color="white"
              variant="outlined"
              prepend-icon="mdi-account-star"
              class="mr-4 text-none"
              density="comfortable"
              @click="crearRecepcionista"
            >
              Crear Recepcionista
            </v-btn>
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
            :items="empleados.concat(profesores).concat(empleadosDesactivados)"
            :search="search"
            :loading="loading"
            loading-text="Cargando personal..."
            no-data-text="No se encontraron empleados"
          >
            <template v-slot:[`item.rol_id`]='{ item }'>
              <v-chip :color="getRoleColor(item.rol_id)" size="small" class="font-weight-bold">
                {{ getRoleName(item.rol_id) }}
              </v-chip>
            </template>

            <template v-slot:[`item.acciones`]='{ item }'>
              <div class="d-flex justify-end">
                <v-btn v-if="!isDisabled"
                  icon="mdi-pencil"
                  variant="text"
                  color="blue-darken-1"
                  size="small"
                  @click="modificarEmpleado(item)"
                  title="Modificar Datos"
                ></v-btn>
                <v-btn v-if="!isDisabled"
                  icon="mdi-shield-key"
                  variant="text"
                  color="orange-darken-2"
                  size="small"
                  @click="abrirEditorRol(item)"
                  title="Cambiar Permisos/Rol"
                ></v-btn>
                <v-btn v-if="!isDisabled"
                  icon="mdi-account-off"
                  variant="text"
                  color="grey-darken-1"
                  size="small"
                  @click="desactivarEmpleado(item)"
                  title="Desactivar"
                ></v-btn>
                <v-btn v-if="!isDisabled"
                  icon="mdi-delete"
                  variant="text"
                  color="red-darken-1"
                  size="small"
                  @click="eliminarEmpleado(item)"
                  title="Eliminar"
                ></v-btn>
                <v-btn v-if="isDisabled"
                  icon="mdi-account-off-outline"
                  variant="text"
                  color="green-darken-1"
                  size="small"
                  @click="activarEmpleado(item)"
                  title="Reactivar Empleado"
                ></v-btn>
              </div>
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

    <!-- Diálogo para Crear Profesor -->
    <v-dialog v-model="dialogProfesor" max-width="500px">
      <v-card rounded="lg">
        <v-card-title class="pa-4 bg-black text-white">Crear Nuevo Profesor</v-card-title>
        <v-card-text class="pt-4">
          <v-form ref="formProfesor">
            <v-text-field v-model="nuevoProfesor.nombre" label="Nombre" variant="outlined" density="comfortable" class="mb-2"></v-text-field>
            <v-text-field v-model="nuevoProfesor.apellido" label="Apellido" variant="outlined" density="comfortable" class="mb-2"></v-text-field>
            <v-text-field v-model="nuevoProfesor.dni" label="DNI" variant="outlined" density="comfortable" type="number"></v-text-field>
          </v-form>
        </v-card-text>
        <v-card-actions class="pa-4">
          <v-spacer></v-spacer>
          <v-btn variant="text" @click="dialogProfesor = false">Cancelar</v-btn>
          <v-btn color="black" variant="elevated" @click="guardarProfesor">Crear Profesor</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Diálogo para Crear Recepcionista -->
    <v-dialog v-model="dialogRecepcionista" max-width="500px">
      <v-card rounded="lg">
        <v-card-title class="pa-4 bg-black text-white">Crear Nuevo Recepcionista</v-card-title>
        <v-card-text class="pt-4">
          <v-form ref="formRecepcionista">
            <v-row>
              <v-col cols="12" sm="6" class="py-1">
                <v-text-field v-model="nuevoRecepcionista.nombre" label="Nombre" variant="outlined" density="comfortable"></v-text-field>
              </v-col>
              <v-col cols="12" sm="6" class="py-1">
                <v-text-field v-model="nuevoRecepcionista.apellido" label="Apellido" variant="outlined" density="comfortable"></v-text-field>
              </v-col>
              <v-col cols="12" class="py-1">
                <v-text-field v-model="nuevoRecepcionista.dni" label="DNI" variant="outlined" density="comfortable" type="number"></v-text-field>
              </v-col>
              <v-col cols="12" class="py-1">
                <v-text-field v-model="nuevoRecepcionista.correo" label="Correo Electrónico" variant="outlined" density="comfortable" prepend-inner-icon="mdi-email"></v-text-field>
              </v-col>
              <v-col cols="12" class="py-1">
                <v-text-field
                  v-model="nuevoRecepcionista.contraseña"
                  label="Contraseña"
                  variant="outlined"
                  density="comfortable"
                  prepend-inner-icon="mdi-lock"
                  type="password"
                ></v-text-field>
              </v-col>
            </v-row>
          </v-form>
        </v-card-text>
        <v-card-actions class="pa-4">
          <v-spacer></v-spacer>
          <v-btn variant="text" @click="dialogRecepcionista = false">Cancelar</v-btn>
          <v-btn color="black" variant="elevated" @click="guardarRecepcionista">Crear Recepcionista</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Dialogo para edicion de empleado -->
    <v-dialog v-model="dialogEditarEmpleado" max-width="600px">
      <EditEmployee :empleado="empleadoSeleccionado" @close="dialogEditarEmpleado = false" @updated="cargarEmpleados" />
    </v-dialog>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { EmployeesService } from '@/services/EmployeesService'
import EditEmployee from './EditEmployee.vue'
import { useNotificationStore } from '@/stores/notificationStore.js'

const empleados = ref([])
const profesores = ref([])
const empleadosDesactivados = ref([])
const search = ref('')
const loading = ref(false)
const dialog = ref(false)
const dialogEditarEmpleado = ref(false)
const empleadoSeleccionado = ref(null)
const nuevoRolId = ref(null)
const isDisabled = ref(false) // Para manejar el estado de desactivación de empleados
const notificationStore = useNotificationStore()

// Estados para creación de personal
const dialogProfesor = ref(false)
const dialogRecepcionista = ref(false)

const nuevoProfesor = ref({
  nombre: '',
  apellido: '',
  dni: ''
})
const nuevoRecepcionista = ref({
  nombre: '',
  apellido: '',
  dni: '',
  correo: '',
  contraseña: ''
})

const headers = [
  { title: 'DNI', key: 'dni', sortable: true },
  { title: 'Nombre', key: 'nombre' },
  { title: 'Apellido', key: 'apellido' },
  { title: 'Correo', key: 'correo' },
  { title: 'Rol Actual', key: 'rol_id', align: 'center' },
  { title: 'Acciones', key: 'acciones', sortable: false, align: 'end' }
]

const roles = [
  { id: 0, label: 'Desactivado' },
  { id: 1, label: 'Administrador' },
  { id: 2, label: 'Recepcionista' },
  { id: 3, label: 'Usuario' }
]

const getRoleName = (id) => roles.find(r => r.id === id)?.label || 'Profesor'
const getRoleColor = (id) => {
  if (id === 0) return 'grey-darken-1' // Empleado desactivado
  if (id === 1) return 'red-darken-1'
  if (id === 2) return 'blue-darken-1'
  return 'green-darken-1' // Color para Profesor
}

const cargarEmpleados = async () => {
  loading.value = true
  try {
    const data = await EmployeesService.getEmployees()
    const fetched = (data || []).map(e => ({
      id: e.id ?? e[0],
      dni: e.dni ?? e[1],
      nombre: e.nombre ?? e[2],
      apellido: e.apellido ?? e[3],
      fecha_nac: e.fecha_nac ?? e[4],
      telefono: e.telefono ?? e[5],
      correo: e.correo ?? e[6],
      genero: e.genero ?? e[8],
      rol_id: e.rol_id ?? e[9]
    }))
    empleados.value = fetched
  } catch (error) {
    console.error('Error cargando empleados:', error)
    empleados.value = []
  } finally {
    loading.value = false
  }
}

const cargarEmpleadosDesactivados = async () => {
  try {
    const data = await EmployeesService.getDisabledEmployees()
    const fetched = (data || []).map(e => ({
      dni: e.dni ?? e[1],
      nombre: e.nombre ?? e[2],
      apellido: e.apellido ?? e[3],
      correo: e.correo ?? e[5],
      rol_id: e.rol_id ?? e[4]
    }))
    empleadosDesactivados.value = fetched
  } catch (error) {
    console.error('Error cargando empleados desactivados:', error)
    empleadosDesactivados.value = []
  }
}

const cargarProfesores = async () => {
  try {
    const resp = await EmployeesService.getProfessors()
    // Depending on backend returning directly an array or { status: "success", data: [...] }
    const resData = resp.data && Array.isArray(resp.data) ? resp.data : (Array.isArray(resp) ? resp : [])
    profesores.value = resData.map(p => ({
      dni: p.dni,
      nombre: p.nombre,
      apellido: p.apellido
    }))
  } catch (error) {
    console.error('Error cargando profesores:', error)
    profesores.value = []
  }
}

const crearProfesor = () => {
  nuevoProfesor.value = { nombre: '', apellido: '', dni: '' }
  dialogProfesor.value = true
}

const guardarProfesor = async () => {
  try {
    if (!nuevoProfesor.value.nombre || !nuevoProfesor.value.dni) {
      notificationStore.showNotification('Por favor complete los campos obligatorios', 'warning')
      return
    }
    await EmployeesService.createProfessor(nuevoProfesor.value)
    notificationStore.showNotification('Profesor creado exitosamente', 'success')
    dialogProfesor.value = false
    await cargarEmpleados()
  } catch (error) {
    console.error('Error al crear profesor:', error)
    notificationStore.showNotification('No se pudo crear el profesor', 'danger')
  }
}

const crearRecepcionista = () => {
  nuevoRecepcionista.value = { nombre: '', apellido: '', dni: '', correo: '', contraseña: '' }
  dialogRecepcionista.value = true
}

const guardarRecepcionista = async () => {
  try {
    if (!nuevoRecepcionista.value.correo || !nuevoRecepcionista.value.contraseña) {
      notificationStore.showNotification('Por favor complete los campos de acceso (correo y contraseña)', 'warning')
      return
    }
    await EmployeesService.createReceptionist(nuevoRecepcionista.value)
    notificationStore.showNotification('Recepcionista creado exitosamente', 'success')
    dialogRecepcionista.value = false
    await cargarEmpleados()
  } catch (error) {
    console.error('Error al crear recepcionista:', error)
    notificationStore.showNotification('No se pudo crear el recepcionista: ' + (error.response?.data?.error || ''), 'danger')
  }
}

const modificarEmpleado = (empleado) => {
  empleadoSeleccionado.value = { ...empleado }
  dialogEditarEmpleado.value = true
}

const desactivarEmpleado = (empleado) => {
  const dni = empleado?.dni ?? empleado?.raw?.dni
  if (!dni) {
    notificationStore.showNotification('No se pudo identificar el DNI del empleado', 'danger')
    return
  }

  notificationStore.showNotification(
    `¿Desactivar a ${empleado.nombre} ${empleado.apellido}?`,
    'warning',
    0, // timeout 0 para que no desaparezca
    async () => {
      try {
        await EmployeesService.deactivateEmployee(dni)
        await cargarEmpleados()
        notificationStore.showNotification('Empleado desactivado exitosamente', 'success')
      } catch (error) {
        console.error('Error al desactivar empleado:', error)
        notificationStore.showNotification('No se pudo desactivar el empleado', 'danger')
      }
    }
  )
}

const eliminarEmpleado = (empleado) => {
  const dni = empleado?.dni
  if (!dni) {
    notificationStore.showNotification('No se pudo identificar el DNI del empleado', 'danger')
    return
  }

  notificationStore.showNotification(
    `Eliminar a ${empleado.nombre} ${empleado.apellido}?`,
    'danger',
    0,
    async () => {
      try {
        await EmployeesService.deleteEmployee(dni)
        await cargarEmpleados() // Refresca la tabla
        notificationStore.showNotification('Empleado eliminado exitosamente', 'success')
      } catch (error) {
        console.error('Error al eliminar empleado:', error)
        const errorMsg = error.data?.error || 'No se pudo eliminar el empleado'
        notificationStore.showNotification(errorMsg, 'danger')
      }
    }
  )
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
    notificationStore.showNotification('Rol actualizado exitosamente', 'success')
  } catch (error) {
    notificationStore.showNotification('Error al actualizar el rol: ' + (error.response?.data?.error || 'Error desconocido'), 'danger')
  }
}

onMounted(() => {
  cargarEmpleados()
  cargarProfesores()
  cargarEmpleadosDesactivados()
})
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
