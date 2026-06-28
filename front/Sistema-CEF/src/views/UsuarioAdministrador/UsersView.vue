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

        
            <v-data-table
              :headers="headers"
              :items="users"
              :search="search"
              :loading="loading"
              loading-text="Cargando usuarios..."
              no-data-text="No se encontraron usuarios"
            >
              <template v-slot:[`item.rol_id`]="{ item }">
                <v-chip :color="getRoleColor(item.rol_id)" size="small" class="font-weight-bold">
                  {{ getRoleName(item.rol_id) }}
                </v-chip>
              </template>

              <template v-slot:[`item.acciones`]="{ item }">
                <div class="d-flex justify-end">
                  <v-btn
                    icon="mdi-pencil"
                    variant="text"
                    color="blue-darken-1"
                    size="small"
                    title="Modificar Datos"
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
        </v-card>
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

const headers = [
  { title: 'DNI', key: 'dni', sortable: true },
  { title: 'Nombre', key: 'nombre' },
  { title: 'Apellido', key: 'apellido' },
  { title: 'Correo', key: 'correo' },
  { title: 'Rol', key: 'rol_id', align: 'center' },
  { title: 'Acciones', key: 'acciones', sortable: false, align: 'end' }
]

const roles = [
  { id: 0, label: 'Desactivado' },
  { id: 1, label: 'Administrador' },
  { id: 2, label: 'Recepcionista' },
  { id: 3, label: 'Usuario' },
  { id: 4, label: 'Eliminado' },
  { id: 5, label: 'Profesor' }
]

const getRoleName = (id) => roles.find(r => r.id === id)?.label || 'Desconocido'
const getRoleColor = (id) => {
  if (id === 3) return 'blue-darken-1' // Usuario
  if (id === 1) return 'green-darken-1' // Admin
  if (id === 2) return 'purple-darken-1' // Recepcionista
  if (id === 5) return 'light-blue-darken-1' // Profesor
  if (id === 4) return 'red-darken-1' // Eliminado
  return 'grey-darken-1' // Desactivado o desconocido
}

const loadUsers = async () => {
  loading.value = true
  try {
    const response = await UsersAdminService.getUsers()
    if (response.status === 'success') {
      // Los datos ya vienen como un array de objetos, solo necesitamos filtrar.
      users.value = response.data.filter(user => user.rol_id === 3)
    }
  } catch (error) {
    notificationStore.showNotification('Error al cargar los usuarios.', 'danger')
    console.error('Error cargando usuarios:', error)
  } finally {
    loading.value = false
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