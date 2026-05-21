<template>
  <v-container class="classes-view" fluid>
    <v-row justify="center">
      <v-col cols="12" md="10">
        <h1 class="text-h4 mb-6 text-center font-weight-bold">Nuestras Clases</h1>

        <div class="d-flex justify-end mb-6">
          <v-btn
            color="blue-darken-1"
            prepend-icon="mdi-plus"
            @click="abrirDialogCrear"
          >
            Publicar Clase
          </v-btn>
        </div>
        
        <v-row>
          <v-col 
            v-for="clase in clases"  
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
                  v-model="nuevaClase.id_actividad"
                  :items="actividades"
                  item-title="nombre"
                  item-value="id"
                  label="Actividad"
                  variant="outlined"
                  density="compact"
                ></v-select>
              </v-col>
              <v-col cols="12" sm="6">
                <v-select
                  v-model="nuevaClase.id_profesor"
                  :items="profesores"
                  item-title="nombre"
                  item-value="id"
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
                  :items="salas"
                  item-title="nombre"
                  item-value="id"
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
import { ref, onMounted } from 'vue'
import { ClasesService } from '@/services/ClasesServices'
import DateFormatterService from '@/services/DateFormatterService.js'

const isEditing = ref(false)
const dialog = ref(false)
const menuFecha = ref(false)



const nuevaClase = ref({
  id_actividad: null, // Usar id_actividad para el v-select
  id_profesor: null,  // Usar id_profesor para el v-select
  fecha: '',
  hora: '',
  sala: ''
})

const clases = ref([])
const actividades = ref([])
const profesores = ref([])
const salas = ref([])

const fetchAuxData = async () => {
  try {
    const [resAct, resProf, resSalas] = await Promise.all([
      ClasesService.listarActividades(),
      ClasesService.listarProfesores(),
      ClasesService.listarSalas()])
    
    if (Array.isArray(resAct)) {
      actividades.value = resAct.map(a => ({ id: a.id ?? a[0], nombre: a.nombre ?? a[1] }))
    }
    if (Array.isArray(resProf)) {
      // El backend devuelve: 0: id, 1: dni, 2: nombre, 3: apellido...
      profesores.value = resProf.map(p => ({ id: p.id ?? p[0], nombre: `${p.nombre ?? p[2]} ${p.apellido ?? p[3]}` }))
    }
    if (Array.isArray(resSalas)) {
      salas.value = resSalas.map(s => ({ id: s.id ?? s[0], nombre: s.nombre ?? s[1] }))
    }
  
  } catch (error) {
    console.error('Error al cargar datos auxiliares:', error)
  }
}

const fetchClases = async () => {
  try {
    const data = await ClasesService.listarClases()
    
    if (!Array.isArray(data)) {
      console.error('Se esperaba un array de clases pero se recibió:', data)
      return
    }

    clases.value = data.map(c => ({
     // Si el backend usa dict(fila), usamos nombres de columnas. 
      // Si todavía usa tuplas, usamos índices como respaldo.
      id: c.id ?? c[0],
      estado: c.estado ?? c[1],
      id_actividad: c.id_actividad ?? c[2],
      id_profesor: c.id_profesor ?? c[3],
      // Resolvemos el ID a un nombre usando las listas cargadas
      categoria: actividades.value.find(a => a.id == (c.id_actividad ?? c[2]))?.nombre 
                 || `ID Act: ${c.id_actividad ?? c[2]}`,
      profesor: profesores.value.find(p => p.id == (c.id_profesor ?? c[3]))?.nombre 
                || `ID Prof: ${c.id_profesor ?? c[3]}`,
      fecha: c.fecha ?? c[4] ?? 'A confirmar',
      hora: c.hora ?? c[5] ?? '--:--',
      sala: c.sala || c[6] || 'Gimnasio',
      imagen: 'https://images.unsplash.com/photo-1534438327276-14e5300c3a48?q=80&w=500'
    }))
  } catch (error) {
    console.error('Error al cargar clases:', error)
  }
}

onMounted(async () => {
  // Cargamos primero los datos auxiliares para poder mapear los nombres después
  await fetchAuxData()
  await fetchClases()
})

const confirmarFecha = (val) => {
  nuevaClase.value.dia = val ? new Date(val).toLocaleDateString() : ''
  menuFecha.value = false
}


const abrirDialogCrear = () => {
  isEditing.value = false
  nuevaClase.value = { id_actividad: null, id_profesor: null, dia: '', hora: '', sala: '' }
  dialog.value = true
}

const cerrarDialog = () => {
  dialog.value = false
  nuevaClase.value = { id_actividad: null, id_profesor: null, dia: '', hora: '', sala: '' }
  dia.value = null
  isEditing.value = false
}

const guardarClase = async () => {
  try {
    const payload = {
      estado: 'Activa',
      id_actividad: nuevaClase.value.id_actividad,
      id_profesor: nuevaClase.value.id_profesor,
      fecha: DateFormatterService.formatDateForBackend(nuevaClase.value.dia),
      hora: nuevaClase.value.hora,
      sala: nuevaClase.value.sala
    }

    if (isEditing.value) {
      await ClasesService.modificarClase(nuevaClase.value.id, payload)
    } else {
      await ClasesService.publicarClase(payload)
    }
    
    await fetchClases() // Recargar la lista
    cerrarDialog()
  } catch (error) {
    console.error('Error al guardar clase:', error)
    alert('Hubo un error al procesar la clase')
  }
}

const editarClase = (clase) => {
  console.log('Editando clase:', clase)
  isEditing.value = true
  nuevaClase.value = { ...clase }
  dialog.value = true
}

const eliminarClase = async (id) => {
  if (confirm('¿Estás seguro de que deseas eliminar esta clase?')) {
    try {
      await ClasesService.eliminarClase(id)
      await fetchClases()
    } catch (error) {
      console.error('Error al eliminar clase:', error)
    }
  }
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