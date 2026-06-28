<template>
  <v-container class="employees-admin" fluid>
    <v-row justify="center">
      <v-col cols="12" md="10">
        <v-card elevation="2" rounded="lg">
          <div class="bg-black text-white">
            <v-card-title class="d-flex align-center pa-4">
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
            <v-card-text class="py-0 d-flex">
              <v-chip-group
                v-model="filtroRol"
                mandatory
                selected-class="text-black bg-white"
                class="mr-4"
              >
                <v-chip value="todos" size="small">Todos</v-chip>
                <v-chip value="admin" size="small">Administradores</v-chip>
                <v-chip value="recepcionista" size="small">Recepcionistas</v-chip>
                <v-chip value="profesor" size="small">Profesores</v-chip>
              </v-chip-group>
              <v-divider vertical></v-divider>
              <v-chip-group
                v-model="filtroEstado"
                mandatory
                selected-class="text-black bg-white"
                class="ml-4"
              >
                <v-chip value="activos" size="small">Activos</v-chip>
                <v-chip value="desactivados" size="small">Desactivados</v-chip>
                <v-chip value="borrados" size="small">Borrados</v-chip>
              </v-chip-group>
            </v-card-text>
          </div>

          <template v-if="empleados.length > 0 || profesores.length > 0">
            <v-data-table
              :headers="headers"
              :items="personalFiltrado"
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
                  <v-btn 
                    icon="mdi-pencil"
                    variant="text"
                    color="blue-darken-1"
                    size="small"
                    :disabled="item.rol_id === 0"
                    @click="modificarEmpleado(item)"
                    title="Modificar Datos"
                  ></v-btn>
                  
                  <v-btn 
                    icon="mdi-shield-key"
                    variant="text"
                    color="orange-darken-2"
                    size="small"
                    :disabled="item.rol_id === 0 || item.rol_id === 5"
                    @click="abrirEditorRol(item)"
                    title="Cambiar Permisos/Rol"
                  ></v-btn>
                  
                  <v-btn 
                    v-if="item.rol_id !== 0"
                    icon="mdi-account-off"
                    variant="text"
                    color="grey-darken-1"
                    size="small"
                    @click="desactivarEmpleado(item)"
                    title="Desactivar"
                  ></v-btn>

                  <v-btn 
                    v-else
                    icon="mdi-account-check"
                    variant="text"
                    color="green-darken-1"
                    size="small"
                    @click="activarEmpleado(item)"
                    title="Reactivar Empleado"
                  ></v-btn>

                  <v-btn
                    icon="mdi-delete"
                    variant="text"
                    color="red-darken-1"
                    size="small"
                    @click="eliminarEmpleado(item)"
                    title="Eliminar"
                  ></v-btn>
                </div>
              </template>
            </v-data-table>
          </template>
          <template v-else>
            <v-row justify="center" class="mt-10 mb-10">
              <v-col cols="12" md="8" class="text-center">
                <v-icon size="64" color="grey-lighten-1" class="mb-4">mdi-account-off</v-icon>
                <div class="text-h5 text-grey-darken-1 font-weight-medium">No existen empleados registrados</div>
              </v-col>
            </v-row>
          </template>
        </v-card>
      </v-col>
    </v-row>
    <v-dialog v-model="dialog" max-width="400px">
      <v-card rounded="lg">
        <v-card-title class="bg-grey-lighten-3">Cambiar Rol de Empleado</v-card-title>
        <v-card-text class="pt-4">
          <div class="mb-4">
            <strong>Empleado:</strong> {{ empleadoSeleccionado?.nombre }} {{ empleadoSeleccionado?.apellido }} 
          </div>
          <v-select
            v-model="nuevoRolId"
            :items="rolesASeleccionar"
            item-title="label"
            item-value="id"
            label="Seleccionar Nuevo Rol"
            variant="outlined"
            class="mb-4"
          ></v-select>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn variant="text" @click="dialog = false">Cancelar</v-btn>
          <v-btn color="black" variant="elevated" @click="confirmarCambioRol">Actualizar</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-dialog v-model="dialogProfesor" max-width="500px">
      <v-card rounded="lg">
        <v-card-title class="pa-4 bg-black text-white">Crear Nuevo Profesor</v-card-title>
        <v-card-text class="pt-4">
          <v-form ref="formProfesor">
            <v-text-field v-model="nuevoProfesor.nombre" label="Nombre" variant="outlined" density="comfortable" class="mb-2"></v-text-field>
            <v-text-field v-model="nuevoProfesor.apellido" label="Apellido" variant="outlined" density="comfortable" class="mb-2"></v-text-field>
            <v-text-field v-model="nuevoProfesor.dni" label="DNI" variant="outlined" density="comfortable" type="number"></v-text-field>
            <v-text-field v-model="nuevoProfesor.telefono" label="Teléfono" variant="outlined" density="comfortable" type="text" class="mt-2"></v-text-field>
            <v-select
              v-model="nuevoProfesor.genero"
              :items="opcionesGenero"
              label="Género"
              variant="outlined"
              density="comfortable"
              class="mt-2"
            ></v-select>
            <v-select
              v-model="nuevoProfesor.actividades"
              :items="actividades"
              item-title="nombre"
              item-value="id"
              label="Actividades que puede dar"
              multiple
              chips
              class="mt-2"
            ></v-select>
          </v-form>
        </v-card-text>
        <v-card-actions class="pa-4">
          <v-spacer></v-spacer>
          <v-btn variant="text" @click="dialogProfesor = false">Cancelar</v-btn>
          <v-btn color="black" variant="elevated" @click="guardarProfesor">Crear Profesor</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

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
              <v-col cols="12" sm="6" class="py-1">
                <v-text-field v-model="nuevoRecepcionista.dni" label="DNI" variant="outlined" density="comfortable" type="number"></v-text-field>
              </v-col>
              <v-col cols="12" sm="6" class="py-1">
                <v-select
                  v-model="nuevoRecepcionista.genero"
                  :items="opcionesGenero"
                  label="Género"
                  variant="outlined"
                  density="comfortable"
                ></v-select>
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

    <v-dialog v-model="dialogEditarEmpleado" max-width="600px">
      <component
        :is="componenteEdicion"
        :empleado="empleadoSeleccionado"
        @close="dialogEditarEmpleado = false"
        @updated="cargarEmpleados"
        :key="empleadoSeleccionado?.dni || 'nuevo'"
      />
    </v-dialog>
  </v-container>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { EmployeesService } from '@/services/EmployeesService'
import { ClasesService } from '@/services/ClasesServices'
import EditEmployee from './EditEmployee.vue'
import EditProfesor from './EditProfesor.vue'
import { useNotificationStore } from '@/stores/notificationStore.js'
import { consoleError } from 'vuetify/lib/util/console.js'

const empleados = ref([])
const profesores = ref([])
const search = ref('')
const loading = ref(false)
const dialog = ref(false)
const filtroRol = ref('todos')
const filtroEstado = ref('activos')
const dialogEditarEmpleado = ref(false)
const empleadoSeleccionado = ref(null)
const nuevoRolId = ref(null)
const nuevoGenero = ref(null)

// Se removió 'isDisabled' de aquí ya que lo evaluamos fila por fila en el template.

const notificationStore = useNotificationStore()

// Estados para creación de personal
const dialogProfesor = ref(false)
const dialogRecepcionista = ref(false)

const opcionesGenero = ['M', 'F', 'O']

const nuevoProfesor = ref({
  nombre: '',
  apellido: '',
  dni: '',
  genero: '',
  telefono: '',
  actividades: []
})
const nuevoRecepcionista = ref({
  nombre: '',
  apellido: '',
  dni: '',
  correo: '',
  contraseña: '',
  genero: ''
})
const actividades = ref([])

const headers = [
  { title: 'DNI', key: 'dni', sortable: true },
  { title: 'Nombre', key: 'nombre' },
  { title: 'Apellido', key: 'apellido' },
  { title: 'Teléfono', key: 'telefono' },
  { title: 'Correo', key: 'correo' },
  { title: 'Género', key: 'genero', align: 'center' },
  { title: 'Rol Actual', key: 'rol_id', align: 'center' },
  { title: 'Acciones', key: 'acciones', sortable: false, align: 'end' }
]

const roles = [
  { id: 0, label: 'Desactivado' },
  { id: 1, label: 'Administrador' },
  { id: 2, label: 'Recepcionista' },
  { id: 3, label: 'Usuario' },
  { id: 4, label: 'Eliminado' }
]

const rolesASeleccionar = [
  { id: 1, label: 'Administrador' },
  { id: 2, label: 'Recepcionista' },
  { id: 3, label: 'Usuario' }
]

const getRoleName = (id) => roles.find(r => r.id === id)?.label || 'Profesor'
const getRoleColor = (id) => {
  if (id === 0) return 'grey-darken-1' // Empleado desactivado
  if (id === 1) return 'green-darken-1'
  if (id === 2) return 'purple-darken-1'
  if (id === 4) return 'red-darken-1' // Empleado eliminado
  return 'light-blue-darken-1' // Color para Profesor
}

const personalFiltrado = computed(() => {
  let listaFiltrada = empleados.value

  // 1. Filtrar por estado
  if (filtroEstado.value === 'activos') {
    // Roles activos son 1 (Admin), 2 (Recepcionista), 5 (Profesor)
    const rolesActivos = [1, 2, 5]
    listaFiltrada = listaFiltrada.filter(e => rolesActivos.includes(e.rol_id))
  } else if (filtroEstado.value === 'desactivados') {
    // Rol desactivado es 0
    listaFiltrada = listaFiltrada.filter(e => e.rol_id === 0)
  } else if (filtroEstado.value === 'borrados') {
    // Rol borrado es 4
    listaFiltrada = listaFiltrada.filter(e => e.rol_id === 4)
  }

  // 2. Filtrar por rol sobre la lista ya filtrada por estado
  if (filtroRol.value === 'todos') {
    return listaFiltrada
  }
  if (filtroRol.value === 'admin') {
    return listaFiltrada.filter(e => e.rol_id === 1)
  }
  if (filtroRol.value === 'recepcionista') {
    return listaFiltrada.filter(e => e.rol_id === 2)
  }
  if (filtroRol.value === 'profesor') {
    return listaFiltrada.filter(e => e.rol_id === 5)
  }

  return listaFiltrada
})

const componenteEdicion = computed(() => {
  const rol = empleadoSeleccionado.value?.rol_id
  const esProfesor = empleadoSeleccionado.value?.esProfesor === true ||
    (rol === 5)

  return esProfesor ? EditProfesor : EditEmployee
})

const cargarEmpleados = async () => {
  loading.value = true
  try {
    const data = await EmployeesService.getEmployees()
    console.log(data)
    const fetched = (data.data).map(e => ({
      apellido: e.apellido ?? e[0],
      correo: e.correo ?? e[1],
      dni: e.dni ?? e[2],
      genero: e.genero ?? e[3],
      id: e.id ?? e[4],
      nombre: e.nombre ?? e[5],
      rol_id: e.rol_id ?? e[6],
      telefono: e.telefono ?? e[7]
    }))

    empleados.value = fetched
    // Se eliminó la validación incorrecta de isDisabled aquí.
  } catch (error) {
    console.error('Error cargando empleados:', error)
    empleados.value = []
  } finally {
    loading.value = false
  }
}

const fetchActividades = async () => {
  try {
    const resAct = await ClasesService.listarActividades()
    if (Array.isArray(resAct)) {
      actividades.value = resAct.map(a => ({ id: a.id ?? a[0], nombre: a.nombre ?? a[1] }))
    }
  } catch (error) {
    console.error('Error al cargar actividades:', error)
  }
}

const crearProfesor = () => {
  nuevoProfesor.value = { nombre: '', apellido: '', dni: '', genero: '', telefono: '', actividades: [] }
  dialogProfesor.value = true
}

const guardarProfesor = async () => {
  try {
    if (!nuevoProfesor.value.nombre || !nuevoProfesor.value.dni || !nuevoProfesor.value.genero || !nuevoProfesor.value.telefono) {
      notificationStore.showNotification('Por favor complete los campos obligatorios', 'warning')
      return
    }
    console.log(nuevoProfesor.value.actividades)
    await EmployeesService.createProfessor(nuevoProfesor.value) // El payload ya incluye las actividades
    notificationStore.showNotification('El profesor fue creado con éxito', 'success')
    dialogProfesor.value = false
    await cargarEmpleados()
  } catch (error) {
    console.error('Error al crear profesor:', error)
    const statusCode = error.status
    if (statusCode === 401) {
      notificationStore.showNotification('Ya existe un empleado con ese DNI', 'danger')
    } else {
      notificationStore.showNotification('No se pudo crear el profesor', 'danger')
    }
  }
}

const crearRecepcionista = () => {
  nuevoRecepcionista.value = { nombre: '', apellido: '', dni: '', correo: '', contraseña: '', genero: '' }
  dialogRecepcionista.value = true
}

const guardarRecepcionista = async () => {
  try {
    if (!nuevoRecepcionista.value.correo || !nuevoRecepcionista.value.contraseña || !nuevoRecepcionista.value.genero) {
      notificationStore.showNotification('Por favor complete todos los campos obligatorios', 'warning')
      return
    }
    await EmployeesService.createReceptionist(nuevoRecepcionista.value)
    notificationStore.showNotification('Se creo el recepcionista exitosamente', 'success')
    dialogRecepcionista.value = false
    await cargarEmpleados()
  } catch (error) {
    console.error('Error al crear recepcionista:', error)
    const statusCode = error.status
    if (statusCode === 401) {
      notificationStore.showNotification('Ya existe un empleado con ese DNI', 'danger')
    } else if (statusCode === 403) {
      notificationStore.showNotification('Ya existe un empleado con ese correo', 'danger')
    } else {
      notificationStore.showNotification('No se pudo crear el recepcionista: ' + ('Error desconocido'), 'danger')
    }
  }
}

const modificarEmpleado = (empleado) => {
  const esProfesor = profesores.value.some(p => p.dni === empleado.dni) ||
    (empleado.rol_id === 5)

  empleadoSeleccionado.value = { ...empleado, esProfesor }
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
    0,
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

// Función añadida para la lógica de Reactivar
const activarEmpleado = (empleado) => {
  const dni = empleado?.dni ?? empleado?.raw?.dni
  if (!dni) return
  
  // Asumiendo que el flujo sea simplemente restaurar el rol (o puedes llamar a tu endpoint correspondiente)
  empleadoSeleccionado.value = empleado
  nuevoRolId.value = 2 // Puedes asignar un rol por defecto o abrir el modal de roles
  dialog.value = true
  notificationStore.showNotification('Por favor asigne un nuevo rol para reactivar al empleado.', 'info')
}

const eliminarEmpleado = (empleado) => {
  console.log(empleado)
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
        await cargarEmpleados()
        notificationStore.showNotification('El empleado fue eliminado con éxito', 'success')
      } catch (error) {
        console.error('Error al eliminar empleado:', error)
        const statusCode = error.status
        if (statusCode === 400) {
          notificationStore.showNotification('El empleado no puede eliminarse si esta asociado a una clase', 'danger')
        } else {
          notificationStore.showNotification('Hubo un error al eliminar el empleado', 'danger')
        }
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
    notificationStore.showNotification('Los permisos fueron modificados exitosamente', 'success')
  } catch (error) {
    const statusCode = error.status
    if (statusCode === 402) {
      notificationStore.showNotification('El empleado ya posee esos permisos', 'danger')
    } else {
      notificationStore.showNotification('Error al actualizar el rol: ' + ('Error desconocido'), 'danger')
    }
  }
}

onMounted(() => {
  cargarEmpleados()
  fetchActividades()
})
</script>

<style scoped>
.employees-admin {
  padding-top: 40px;
  background-color: var(--bg-main); /* Fallback a gris claro si la variable no está definida */
  min-height: 100vh;
}
.search-field :deep(.v-field__input) {
  color: black !important;
}
</style>