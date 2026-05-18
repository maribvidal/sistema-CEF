<template>
  <v-container class="classes-view" fluid>
    <v-row justify="center">
      <v-col cols="12" md="10">
        <h1 class="text-h4 mb-6 text-center font-weight-bold">Nuestras Clases</h1>

        <div class="d-flex justify-end mb-6">
          <v-btn
            color="black"
            prepend-icon="mdi-plus"
            @click="abrirDialogCrear"
          >
            Publicar Clase
          </v-btn>
        </div>
        
        <v-row>
          <v-col 
            v-for="clase in clasesMock" 
            :key="clase.id" 
            cols="12"
          >
            <v-card class="class-card-horizontal" elevation="2" rounded="lg">
              <v-row no-gutters>
                <!-- Imagen de la clase -->
                <v-col cols="12" md="4" sm="5">
                  <v-img
                    :src="clase.imagen"
                    height="175"
                    cover
                    class="class-image"
                  >
                    <div class="d-flex fill-height align-end">
                      <v-card-title class="class-title-overlay text-uppercase font-weight-black w-100">
                        {{ clase.categoria }}
                      </v-card-title>
                    </div>
                  </v-img>
                </v-col>

                <!-- Contenido de la clase -->
                <v-col cols="12" md="5" sm="7" class="pa-2 d-flex flex-column justify-center">
                  <div class="d-flex align-center mb-1">
                    <v-icon size="small" class="mr-2" color="red-darken-2">mdi-account-tie</v-icon>
                    <span class="text-body-1 font-weight-bold">Profesor:</span>
                    <span class="text-body-1 ml-2">{{ clase.profesor }}</span>
                  </div>

                  <div class="d-flex align-center mb-1">
                    <v-icon size="small" class="mr-2" color="red-darken-2">mdi-calendar-range</v-icon>
                    <span class="text-body-1 font-weight-bold">Día:</span>
                    <span class="text-body-1 ml-2">{{ clase.dia }}</span>
                  </div>

                  <div class="d-flex align-center mb-1">
                    <v-icon size="small" class="mr-2" color="red-darken-2">mdi-clock-outline</v-icon>
                    <span class="text-body-1 font-weight-bold">Hora:</span>
                    <span class="text-body-1 ml-2">{{ clase.hora }}</span>
                  </div>

                  <div class="d-flex align-center">
                    <v-icon size="small" class="mr-2" color="red-darken-2">mdi-map-marker-outline</v-icon>
                    <span class="text-body-1 font-weight-bold">Sala:</span>
                    <span class="text-body-1 ml-2">{{ clase.sala }}</span>
                  </div>
                </v-col>

                <!-- Acciones -->
                <v-divider vertical class="hidden-sm-and-down"></v-divider>
                <v-col cols="12" md="3" class="pa-0 d-flex flex-column">
                  <v-btn
                    color="success"
                    variant="tonal"
                    prepend-icon="mdi-calendar-check"
                    
                    size="x-small"
                    density="compact"
                    rounded="0"
                    class="flex-grow-1"
                    @click="reservarClase(clase.id)"
                  >
                    Reservar Clase
                  </v-btn>
                  <v-btn
                    color="orange-darken-1"
                    variant="tonal"
                    prepend-icon="mdi-calendar-remove"
                    size="x-small"
                    density="compact"
                    rounded="0"
                    class="flex-grow-1"
                    @click="cancelarReserva(clase.id)"
                  >
                    Cancelar Reserva
                  </v-btn>
                  <v-btn
                    color="blue-darken-1"
                    variant="tonal"
                    prepend-icon="mdi-pencil"
                    size="x-small"
                    density="compact"
                    rounded="0"
                    class="flex-grow-1"
                    @click="editarClase(clase)"
                  >
                    Editar Clase
                  </v-btn>
                  <v-btn
                    color="orange-darken-1"
                    variant="tonal"
                    prepend-icon="mdi-close-circle"
                    size="x-small"
                    density="compact"
                    rounded="0"
                    class="flex-grow-1"
                    @click="cancelarClase(clase.id)"
                  >
                    Cancelar Clase
                  </v-btn>
                  <v-btn
                    color="red-darken-1"
                    variant="tonal"
                    prepend-icon="mdi-delete"
                    size="x-small"
                    density="compact"
                    rounded="0"
                    class="flex-grow-1"
                    @click="eliminarClase(clase.id)"
                  >
                    Eliminar Clase
                  </v-btn>
                </v-col>
              </v-row>
            </v-card>
          </v-col>
        </v-row>
      </v-col>
    </v-row>

    <!-- Diálogo para publicar nueva clase -->
    <v-dialog v-model="dialog" max-width="600px" persistent>
      <v-card rounded="lg">
        <v-card-title class="pa-4 bg-black text-white">
          <span class="text-h5">{{ isEditing ? 'Editar Clase' : 'Publicar Nueva Clase' }}</span>
        </v-card-title>
        <v-card-text class="pt-4">
          <v-form>
            <v-row>
              <v-col cols="12" sm="6">
                <v-select
                  v-model="nuevaClase.categoria"
                  :items="['Yoga', 'Funcional', 'Pilates']"
                  label="Actividad"
                  variant="outlined"
                  density="compact"
                ></v-select>
              </v-col>
              <v-col cols="12" sm="6">
                <v-select
                  v-model="nuevaClase.profesor"
                  :items="['Lucas Gómez', 'Elena Paz', 'Marcos Rueda']"
                  label="Profesor"
                  variant="outlined"
                  density="compact"
                ></v-select>
              </v-col>
              <v-col cols="12" sm="6">
                <v-menu v-model="menuFecha" :close-on-content-click="false">
                  <template v-slot:activator="{ props }">
                    <v-text-field
                      v-model="nuevaClase.dia"
                      label="Seleccionar Día"
                      prepend-inner-icon="mdi-calendar"
                      readonly
                      v-bind="props"
                      variant="outlined"
                      density="compact"
                    ></v-text-field>
                  </template>
                  <v-date-picker v-model="fechaSeleccionada" @update:model-value="confirmarFecha"></v-date-picker>
                </v-menu>
              </v-col>
              <v-col cols="12" sm="6">
                <v-text-field v-model="nuevaClase.hora" label="Hora" type="time" variant="outlined" density="compact"></v-text-field>
              </v-col>
              <v-col cols="12" sm="6">
                <v-select
                  v-model="nuevaClase.sala"
                  :items="['1', '2', '3']"
                  label="Sala"
                  variant="outlined"
                  density="compact"
                ></v-select>
              </v-col>
            </v-row>
          </v-form>
        </v-card-text>
        <v-divider></v-divider>
        <v-card-actions class="pa-4">
          <v-spacer></v-spacer>
          <v-btn color="grey-darken-1" variant="text" @click="cerrarDialog">Cancelar</v-btn>
          <v-btn color="black" variant="elevated" @click="guardarClase">Guardar Clase</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script setup>
import { ref } from 'vue'

const isEditing = ref(false)
const dialog = ref(false)
const menuFecha = ref(false)
const fechaSeleccionada = ref(null)

const nuevaClase = ref({
  categoria: '',
  profesor: '',
  dia: '',
  hora: '',
  sala: ''
})

const confirmarFecha = (val) => {
  nuevaClase.value.dia = val ? new Date(val).toLocaleDateString() : ''
  menuFecha.value = false
}

// Datos de prueba (Mock data) para el diseño
const clasesMock = ref([
  {
    id: 1,
    categoria: 'Funcional',
    profesor: 'Lucas Gómez',
    dia: 'Lunes',
    hora: '08:00',
    sala: 'Sala 1',
    imagen: 'https://images.unsplash.com/photo-1534438327276-14e5300c3a48?q=80&w=500'
  },
  {
    id: 2,
    categoria: 'Yoga',
    profesor: 'Elena Paz',
    dia: 'Martes',
    hora: '10:00',
    sala: 'Sala 2',
    imagen: 'https://images.unsplash.com/photo-1544367567-0f2fcb009e0b?q=80&w=500'
  },
  {
    id: 3,
    categoria: 'Pilates',
    profesor: 'Marcos Rueda',
    dia: 'Miércoles',
    hora: '19:00',
    sala: 'Sala 3',
    imagen: 'https://images.unsplash.com/photo-1534258936925-c58bed479fcb?q=80&w=500'
  }
  ])

const abrirDialogCrear = () => {
  isEditing.value = false
  nuevaClase.value = { categoria: '', profesor: '', dia: '', hora: '', sala: '' }
  dialog.value = true
}

const cerrarDialog = () => {
  dialog.value = false
  nuevaClase.value = { categoria: '', profesor: '', dia: '', hora: '', sala: '' }
  fechaSeleccionada.value = null
  isEditing.value = false
}

const guardarClase = () => {
  console.log('Simulando guardado de clase:', nuevaClase.value)
  const accion = isEditing.value ? 'Actualizando' : 'Creando'
  console.log(`${accion} clase:`, nuevaClase.value)
  cerrarDialog()
}

const editarClase = (clase) => {
  console.log('Editando clase:', clase)
  isEditing.value = true
  nuevaClase.value = { ...clase }
  dialog.value = true
}

const eliminarClase = (id) => {
  console.log('Eliminando clase con ID:', id)
}

const cancelarClase = (id) => {
  console.log('Cancelando clase con ID:', id)
}

const reservarClase = (id) => {
  console.log('Reservando clase con ID:', id)
}

const cancelarReserva = (id) => {
  console.log('Cancelando reserva de clase con ID:', id)
}
</script>

<style scoped>
.classes-view {
  padding-top: 40px;
  background-color: #f5f5f5; /* Fondo gris claro para que resalten las cards blancas */
  min-height: 100vh;
}

.class-card-horizontal {
  border-radius: 12px;
  overflow: hidden;
  transition: transform 0.3s ease;
}

.class-card-horizontal:hover {
  transform: scale(1.01);
}

.class-title-overlay {
  background: linear-gradient(to top, rgba(0, 0, 0, 0.7) 0%, rgba(0, 0, 0, 0) 100%);
  color: white;
  padding: 12px 12px 4px 12px !important;
  font-size: 1.1rem !important;
  letter-spacing: 1px;
  width: 100%;
}
</style>