<template>
  <v-container class="users-admin" fluid>
    <v-row justify="center">
      <v-col cols="12" md="10">
        <v-card elevation="2" rounded="lg">
          <div class="bg-black text-white">
            <v-card-title class="d-flex align-center pa-4">
              <v-icon icon="mdi-account-cog" class="mr-3"></v-icon>
              <span class="text-h5">Administración de Usuarios</span>
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
          </div>

          <template v-if="users.length > 0">
            <v-data-table
              :headers="headers"
              :items="users"
              :search="search"
              :loading="loading"
              :header-props="{ class: 'font-weight-bold' }"
              loading-text="Cargando usuarios..."
              no-data-text="No se encontraron usuarios"
            >
              <template v-slot:[`item.acciones`]="{ item }">
                <div class="d-flex justify-end">
                   <v-btn 
                    icon="mdi-calendar-month"
                    variant="text"
                    color="orange-darken-2"
                    size="small"
                    title="Cambiar fecha de mensualidad"
                    @click="handleChangeMonthlyPayment(item)"
                  ></v-btn>
                   <v-btn 
                    icon="mdi-account-off"
                    variant="text"
                    color="grey-darken-1"
                    size="small"
                    title="Desactivar"
                  ></v-btn>
                  <v-btn
                    icon="mdi-delete"
                    variant="text"
                    color="red-darken-1"
                    size="small"
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
                <div class="text-h5 text-grey-darken-1 font-weight-medium">No existen usuarios registrados</div>
              </v-col>
            </v-row>
          </template>
        </v-card>
        <v-dialog v-model="dialog" max-width="500px">
          <v-card>
            <v-card-title class="text-h5">Cambiar Fecha de Mensualidad</v-card-title>
            <v-card-text>
              <v-form ref="form" v-model="formValid">
                <v-text-field
                  v-model="fechaFin"
                  label="Nueva Fecha de Fin"
                  type="date"
                  :rules="[value => !!value || 'La fecha es requerida']"
                  required
                ></v-text-field>
              </v-form>
            </v-card-text>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn text @click="dialog = false">Cancelar</v-btn>
              <v-btn color="primary" :disabled="!formValid" @click="submitChange">Guardar</v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { UsersAdminService } from '@/services/UsuariosServices.js'
import { useNotificationStore } from '@/stores/notificationStore.js'

const users = ref([])
const search = ref('')
const loading = ref(false)
const notificationStore = useNotificationStore()

const dialog = ref(false)
const fechaFin = ref('')
const formValid = ref(false)
const form = ref(null)
const usuarioSeleccionado = ref(null)

const headers = [
  { title: 'DNI', key: 'dni', sortable: true },
  { title: 'Nombre', key: 'nombre' },
  { title: 'Apellido', key: 'apellido' },
  { title: 'Teléfono', key: 'telefono' },
  { title: 'Correo', key: 'correo' },
  { title: 'Género', key: 'genero', align: 'center' },
  { title: 'Acciones', key: 'acciones', sortable: false, align: 'end' }
]

const loadUsers = async () => {
  loading.value = true
  try {
    const response = await UsersAdminService.getUsers();
    const data = response || [];
    console.log(response)
    const fetchedUsers = data.map(u => ({
      apellido: u.apellido ?? u[0],
      correo: u.correo ?? u[1],
      dni: u.dni ?? u[2],
      fecha_nac: u.fecha_nac ?? u[3],
      genero: u.genero ?? u[4],
      id: u.id ?? u[5],
      nombre: u.nombre ?? u[6],
      rol_id: u.rol_id ?? u[7],
      telefono: u.telefono ?? u[8]
    }));

    users.value = fetchedUsers.filter(user => user.rol_id === 3);
  } catch (error) {
    notificationStore.showNotification('Error al cargar los usuarios.', 'danger')
    console.error('Error cargando usuarios:', error)
  } finally {
    loading.value = false
  }
}

const handleChangeMonthlyPayment = async (item) => {
  try {
    const mensualidad = await UsersAdminService.getMensualidadUsuario(item.dni)
    console.log('mensualidad:', mensualidad) // para ver la estructura y confirmar el campo id
    usuarioSeleccionado.value = {
      ...item,
      id_mensualidad: mensualidad.id // ajustá el campo según lo que devuelva el log
    }
    fechaFin.value = ''
    dialog.value = true
  } catch (responseError) {
    notificationStore.showNotification('Este usuario no tiene una mensualidad activa.', 'danger')
  }
}

const submitChange = async () => {
  try {
    await UsersAdminService.configureMonthlyPayment(
      usuarioSeleccionado.value.dni,
      usuarioSeleccionado.value.id_mensualidad, // 👈 ahora viene del endpoint
      fechaFin.value
    )
    notificationStore.showNotification('Fecha de mensualidad actualizada correctamente.', 'success')
    dialog.value = false
  } catch (error) {
    notificationStore.showNotification('Error al actualizar la fecha de mensualidad.', 'danger')
  }
}

onMounted(() => {
  loadUsers()

})
</script>

<style scoped>
.users-admin {
  padding-top: 40px;
  background-color: var(--bg-main, #f5f5f5);
  min-height: 100vh;
}
.search-field :deep(.v-field__input) {
  color: black !important;
}
</style>