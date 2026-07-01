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
            </v-card-title>
            <v-card-text class="py-0 d-flex">
              <v-chip-group
                v-model="filtroEstado"
                mandatory
                selected-class="text-black bg-white"
              >
                <v-chip value="todos" size="small">Todos</v-chip>
                <v-chip value="activos" size="small">Activos</v-chip>
                <v-chip value="desactivados" size="small">Desactivados</v-chip>
                <v-chip value="borrados" size="small">Borrados</v-chip>
              </v-chip-group>
            </v-card-text>
          </div>

          <template v-if="users.length > 0">
            <v-data-table
              :headers="headers"
              :items="usuariosFiltrados"
              :search="search"
              :loading="loading"
              :header-props="{ class: 'font-weight-bold' }"
              loading-text="Cargando usuarios..."
              no-data-text="No se encontraron usuarios"
            >
              <template v-slot:[`item.rol_id`]="{ item }">
                <v-chip :color="getStatusColor(item.rol_id)" size="small" class="font-weight-bold">
                  {{ getStatusName(item.rol_id) }}
                </v-chip>
              </template>
              <template v-slot:[`item.acciones`]="{ item }">
                <div class="d-flex justify-end">
                   <v-btn 
                    v-if="item.rol_id < 10"
                    icon="mdi-calendar-month"
                    variant="text"
                    color="orange-darken-2"
                    size="small"
                    title="Cambiar fecha de mensualidad"
                    @click="handleChangeMonthlyPayment(item)"
                  ></v-btn>
                  <v-btn
                    v-if="item.rol_id < 20"
                    icon="mdi-account-off"
                    :variant="item.rol_id < 10 ? 'text' : 'tonal'"
                    :color="item.rol_id < 10 ? 'grey-darken-1' : 'green-darken-1'"
                    size="small"
                    :title="item.rol_id < 10 ? 'Desactivar' : 'Reactivar Usuario'"
                    @click="item.rol_id < 10 ? deactivateUser(item) : reactivateUser(item)"
                  ></v-btn>
                  <v-btn
                    v-if="item.rol_id < 20"
                    icon="mdi-delete"
                    variant="text"
                    color="red-darken-1"
                    size="small"
                    title="Eliminar"
                    @click="handleDeleteUser(item)"
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

        <v-dialog v-model="dialogMotivoEliminacionUsuario" max-width="500px">
          <v-card rounded="lg">
            <v-card-title class="bg-grey-lighten-3">Motivo de Eliminación</v-card-title>
            <v-card-text class="pt-4">
              <v-form>
                <v-textarea
                  v-model="motivoEliminacion"
                  label="Ingrese el motivo de eliminación del usuario"
                  variant="outlined"
                  density="comfortable"
                  rows="4"
                ></v-textarea>
              </v-form>
            </v-card-text>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn variant="text" @click="dialogMotivoEliminacionUsuario = false">Cancelar</v-btn>
              <v-btn color="red-darken-1" variant="elevated" @click="confirmDeleteUser">Eliminar</v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { UsersAdminService } from '@/services/UsuariosServices.js'
import { useNotificationStore } from '@/stores/notificationStore.js'

const users = ref([])
const search = ref('')
const loading = ref(false)
const notificationStore = useNotificationStore()

const filtroEstado = ref('todos')
const dialog = ref(false)
const fechaFin = ref('')
const formValid = ref(false)
const form = ref(null)
const usuarioSeleccionado = ref(null)

// Estados para eliminación de usuario
const dialogMotivoEliminacionUsuario = ref(false)
const motivoEliminacion = ref('')
const usuarioAEliminar = ref(null)

const headers = [
  { title: 'DNI', key: 'dni', sortable: true },
  { title: 'Nombre', key: 'nombre' },
  { title: 'Apellido', key: 'apellido' },
  { title: 'Teléfono', key: 'telefono' },
  { title: 'Correo', key: 'correo' },
  { title: 'Género', key: 'genero', align: 'center' },
  { title: 'Rol', key: 'rol_id', align: 'center' },
  { title: 'Acciones', key: 'acciones', sortable: false, align: 'end' }
]

const usuariosFiltrados = computed(() => {
  const listaCompleta = users.value

  switch (filtroEstado.value) {
    case 'activos':
      return listaCompleta.filter(u => u.rol_id > 0 && u.rol_id < 10)
    case 'desactivados':
      return listaCompleta.filter(u => u.rol_id >= 10 && u.rol_id < 20)
    case 'borrados':
      return listaCompleta.filter(u => u.rol_id >= 20)
    case 'todos':
    default:
      return listaCompleta
  }
})

const getStatusName = (id) => {
  return 'Usuario'
}

const getStatusColor = (id) => {
  if (id >= 20) return 'red-darken-1'
  if (id >= 10) return 'grey-darken-1'
  return 'green-darken-1'
}

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

    users.value = fetchedUsers.filter(user => user.rol_id % 10 === 3);
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
    usuarioSeleccionado.value = {
      ...item,
      id_mensualidad: mensualidad.message[0].id // 👈 corrección
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

const deactivateUser = (user) => {
  if (!user.id) {
    notificationStore.showNotification('No se pudo identificar al usuario.', 'danger');
    return;
  }

  notificationStore.showNotification(
    `¿Desactivar a ${user.nombre} ${user.apellido}?`,
    'warning',
    0, // Timeout 0 para que sea persistente
    async () => {
      try {
        await UsersAdminService.deactivateUser(user.id);
        notificationStore.showNotification('Usuario desactivado correctamente.', 'success');
        await loadUsers(); // Recargar la lista de usuarios
      } catch (error) {
        console.error('Error al desactivar usuario:', error);
        notificationStore.showNotification('Hubo un error al desactivar el usuario.', 'danger');
      }
    }
  );
};

const reactivateUser = (user) => {
  if (!user.id) {
    notificationStore.showNotification('No se pudo identificar al usuario.', 'danger');
    return;
  }

  notificationStore.showNotification(
    `¿Reactivar a ${user.nombre} ${user.apellido}?`,
    'info',
    0,
    async () => {
      try {
        await UsersAdminService.reactivateUser(user.id);
        notificationStore.showNotification('Usuario reactivado correctamente.', 'success');
        await loadUsers();
      } catch (error) {
        console.error('Error al reactivar usuario:', error);
        notificationStore.showNotification('Hubo un error al reactivar el usuario.', 'danger');
      }
    }
  );
};

const handleDeleteUser = (user) => {
  if (!user.id) {
    notificationStore.showNotification('No se pudo identificar al usuario.', 'danger');
    return;
  }
  usuarioAEliminar.value = user;
  motivoEliminacion.value = '';
  dialogMotivoEliminacionUsuario.value = true;
};

const confirmDeleteUser = async () => {
  if (!motivoEliminacion.value.trim()) {
    notificationStore.showNotification('Por favor, ingrese un motivo de eliminación.', 'warning');
    return;
  }

  dialogMotivoEliminacionUsuario.value = false;

  notificationStore.showNotification(
    `¿Eliminar permanentemente a ${usuarioAEliminar.value.nombre} ${usuarioAEliminar.value.apellido}?`,
    'danger',
    0,
    async () => {
      try {
      await UsersAdminService.deleteUser(user.id);
        notificationStore.showNotification('Usuario eliminado correctamente.', 'success');
        await loadUsers(); // Recargar la lista de usuarios
      } catch (error) {
        console.error('Error al eliminar usuario:', error);
        notificationStore.showNotification('Hubo un error al eliminar el usuario.', 'danger');
      }
    }
  );
};

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