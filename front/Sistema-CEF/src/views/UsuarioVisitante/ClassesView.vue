<template>
  <v-container class="classes-view" fluid>
    <v-row justify="center">
      <v-col cols="12" md="10">
        <h1 class="text-h4 mb-6 text-center font-weight-bold">Nuestras Clases</h1>

        <div 
          v-if="userRole === 1 || userRole === 2" 
          class="d-flex justify-center justify-md-end mb-6"
        >
          <v-btn
            color="blue-darken-1"
            prepend-icon="mdi-plus"
            @click="abrirDialogCrear"
          >
            Publicar Clase
          </v-btn>
        </div>
        
        <v-row v-if="clases.length > 0">
          <v-col 
            v-for="clase in clases"  
            :key="clase.id" 
            cols="12"
          >
            <v-card class="class-card-horizontal" elevation="2" rounded="lg">
              <v-row no-gutters>
                <v-col cols="12" md="4" sm="5">
                  <v-img
                    :src="clase.imagen"
                    :height="$vuetify.display.xs ? 200 : 175"
                    cover
                    class="class-image"
                  >
                    <v-chip
                      v-if="clase.estado === 'Cancelada' || clase.estado === 'Borrado'"
                      :color="clase.estado === 'Cancelada' ? 'red-darken-4' : 'grey-darken-3'"
                      class="ma-2 font-weight-bold"
                      style="position: absolute; top: 0; right: 0; z-index: 1;"
                      label
                    >
                      {{ clase.estado.toUpperCase() }}
                    </v-chip>
                    <div class="d-flex fill-height align-end">
                      <v-card-title class="class-title-overlay text-uppercase font-weight-black w-100">
                        {{ clase.categoria }}
                      </v-card-title>
                    </div>
                  </v-img>
                </v-col>

                <v-col cols="12" md="5" sm="7" :class="$vuetify.display.mdAndUp ? 'pa-2' : 'pa-4'" class="d-flex flex-column justify-center">
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

                  <div class="d-flex align-center mb-1">
                    <v-icon size="small" class="mr-2" color="red-darken-2">mdi-map-marker-outline</v-icon>
                    <span class="text-body-1 font-weight-bold">Sala:</span>
                    <span class="text-body-1 ml-2">{{ clase.sala_nombre }}</span>
                  </div>

                  <div class="d-flex align-center">
                    <v-icon size="small" class="mr-2" color="red-darken-2">mdi-account-multiple</v-icon>
                    <span class="text-body-1 font-weight-bold">Cupo Máximo:</span>
                    <span class="text-body-1 ml-2">{{ clase.cupo_maximo }} personas</span>
                  </div>
                </v-col>

                <v-divider vertical class="hidden-sm-and-down"></v-divider>
                <v-col cols="12" md="3" :class="$vuetify.display.mdAndUp ? 'pa-0' : 'pa-4 ga-2 bg-grey-lighten-4'" class="d-flex flex-column justify-center bg-md-transparent">
                  
                  <v-btn
                    color="success"
                    :variant="$vuetify.display.mdAndUp ? 'tonal' : 'elevated'"
                    prepend-icon="mdi-calendar-check"
                    :size="$vuetify.display.mdAndUp ? 'x-small' : 'small'"
                    :density="$vuetify.display.mdAndUp ? 'compact' : 'default'"
                    :rounded="$vuetify.display.mdAndUp ? '0' : 'lg'"
                    block
                    :class="{ 'flex-grow-1': $vuetify.display.mdAndUp }"
                    v-if="userRole === 3 && !clase.yaReservada"
                    @click="reservarClase(clase)"
                  >
                    Reservar Clase
                  </v-btn>

                  <v-btn
                    color="orange-darken-1"
                    :variant="$vuetify.display.mdAndUp ? 'tonal' : 'outlined'"
                    prepend-icon="mdi-calendar-remove"
                    :size="$vuetify.display.mdAndUp ? 'x-small' : 'small'"
                    :density="$vuetify.display.mdAndUp ? 'compact' : 'default'"
                    :rounded="$vuetify.display.mdAndUp ? '0' : 'lg'"
                    block
                    :class="{ 'flex-grow-1': $vuetify.display.mdAndUp }"
                    v-if="userRole === 3 && clase.yaReservada"
                    @click="cancelarReserva(clase)"
                  >
                    Cancelar Reserva
                  </v-btn>

                  <v-btn
                    color="blue-darken-1"
                    variant="tonal"
                    prepend-icon="mdi-pencil"
                    :size="$vuetify.display.mdAndUp ? 'x-small' : 'small'"
                    :density="$vuetify.display.mdAndUp ? 'compact' : 'default'"
                    :rounded="$vuetify.display.mdAndUp ? '0' : 'lg'"
                    block
                    :class="{ 'flex-grow-1': $vuetify.display.mdAndUp }"
                    @click="editarClase(clase)"
                    v-if="userRole === 1 || userRole === 2"
                  >
                    Editar Clase
                  </v-btn>
                  
                  <v-btn
                    color="orange-darken-1"
                    variant="tonal"
                    prepend-icon="mdi-close-circle"
                    :size="$vuetify.display.mdAndUp ? 'x-small' : 'small'"
                    :density="$vuetify.display.mdAndUp ? 'compact' : 'default'"
                    :rounded="$vuetify.display.mdAndUp ? '0' : 'lg'"
                    block
                    :class="{ 'flex-grow-1': $vuetify.display.mdAndUp }"
                    @click="cancelarClase(clase)"
                    v-if="userRole === 1 || userRole === 2"
                  >
                    Cancelar Clase
                  </v-btn>
                  
                  <v-btn
                    color="red-darken-1"
                    variant="tonal"
                    prepend-icon="mdi-delete"
                    :size="$vuetify.display.mdAndUp ? 'x-small' : 'small'"
                    :density="$vuetify.display.mdAndUp ? 'compact' : 'default'"
                    :rounded="$vuetify.display.mdAndUp ? '0' : 'lg'"
                    block
                    :class="{ 'flex-grow-1': $vuetify.display.mdAndUp }"
                    @click="eliminarClase(clase)"
                    v-if="userRole === 1 || userRole === 2"
                  >
                    Eliminar Clase
                  </v-btn>
                </v-col>
              </v-row>
            </v-card>
          </v-col>
        </v-row>

        <v-row v-else justify="center" class="mt-10">
          <v-col cols="12" md="8" class="text-center">
            <v-icon size="64" color="grey-lighten-1" class="mb-4">mdi-calendar-search</v-icon>
            <div class="text-h5 text-grey-darken-1 font-weight-medium">No hay ninguna clase publicada de momento</div>
          </v-col>
        </v-row>
      </v-col>
    </v-row>

    <v-dialog v-model="dialog" max-width="600px" persistent>
      <v-card rounded="lg">
        <v-card-title class="pa-4 bg-black text-white">
          <span class="text-h5">{{ isEditing ? 'Editar Clase' : 'Publicar Nueva Clase' }}</span>
        </v-card-title>
        <v-card-text class="pt-4">
          <v-form>
            <v-row>
              <v-col cols="12" sm="6" v-if="!isEditing">
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
              <v-col cols="12" sm="6" v-if="!isEditing">
                <v-select
                  v-model="nuevaClase.dia"
                  :items="diasSemana"
                  label="Día de la Semana"
                  variant="outlined"
                  density="compact"
                ></v-select>
              </v-col>
              <v-col cols="12" sm="6" v-if="!isEditing">
                <v-select
                  v-model="horaSel"
                  :items="horas"
                  label="Hora"
                  variant="outlined"
                  density="compact"
                ></v-select>
              </v-col>
              <v-col cols="12" sm="6">
                <v-select
                  v-model="nuevaClase.id_sala"
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
          <v-btn 
            color="black" 
            variant="elevated" 
            @click="isEditing ? actualizarClase() : crearClase()"
          >Guardar Clase</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script setup>
import { ref, onMounted, watch, computed } from 'vue'
import { ClasesService } from '@/services/ClasesServices'
// IMPORTANTE: Asegúrate de que UsuariosService exporte la función obtenerClase

import { useNotificationStore } from '@/stores/notificationStore.js'
import { useAuth } from '@/services/UsuariosServices.js'
const { userProfile, userRole } = useAuth()
const isEditing = ref(false)
const dialog = ref(false)
const notificationStore = useNotificationStore()
const horas = Array.from({ length: 24 }, (_, i) => i.toString().padStart(2, '0'))
const horaSel = ref('08')

const clasesReservadasIds = ref([]) // Estado para guardar las IDs de clases del usuario

watch(horaSel, (h) => {
  nuevaClase.value.hora = `${h}:00`
})

const nuevaClase = ref({
  id_actividad: null,
  id_profesor: null,
  id_sala: '', 
  dia: '',
  hora: '',
  cupo_maximo: ''
})

const clases = ref([])
const actividades = ref([])
const profesores = ref([])
const salas = ref([])
const diasSemana = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']

const fetchAuxData = async () => {
  try {
    const [resAct, resProf, resSalas] = await Promise.all([
      ClasesService.listarActividades(),
      ClasesService.listarProfesores(),
      ClasesService.listarSalas()
    ])
    
    if (Array.isArray(resAct)) {
      actividades.value = resAct.map(a => ({ id: a.id ?? a[0], nombre: a.nombre ?? a[1] }))
    }
    if (Array.isArray(resProf)) {
      profesores.value = resProf.map(p => ({ id: p.id ?? p[0], nombre: `${p.nombre ?? p[2]} ${p.apellido ?? p[3]}` }))
    }
    if (Array.isArray(resSalas)) {
      salas.value = resSalas.map(s => ({ id: s.id ?? s[0], nombre: s.nombre ?? s[1] }))
    }
  } catch (error) {
    console.error('Error al cargar datos auxiliares:', error)
  }
}

// Nueva función para obtener las clases a las que el usuario ya se anotó
const fetchClasesUsuario = async () => {
  // Solo consultamos si es un cliente (rol 3) y tenemos su ID
  if (userRole.value === 3 && userProfile.value?.id) {
    try {
      // Usamos la función que me indicaste
      const response = await ClasesService.obtenerClase(userProfile.value.id)
      const misClases = response.data || response // Ajusta según la estructura de Axios
      
      if (Array.isArray(misClases)) {
        clasesReservadasIds.value = misClases.map(c => c.id ?? c[0])
      }
    } catch (error) {
      console.error('Error al cargar clases del usuario:', error)
    }
  }
}

const fetchClases = async () => {
  try {
    const data = await ClasesService.listarClases()
    
    if (!Array.isArray(data)) {
      console.error('Se esperaba un array de clases pero se recibió:', data)
      return
    }
    
    clases.value = data.map(c => {
      const claseId = c.id ?? c[0];
      return {
        id: claseId,
        id_actividad: c.actividad_id ?? c[2],
        estado: c.estado ?? c[1],
        dia: c.dia ?? c.fecha ?? c[4] ?? 'A confirmar',
        hora: (c.hora ?? c[5]) ?? '--:--',
        id_profesor: c.profesor_id ?? c[3], // Ensure this is id_profesor
        sala: c.sala_id ?? c[6],
        cupo_maximo: c.cupo_maximo ?? c[7],
        categoria: actividades.value.find(a => a.id == (c.actividad_id ?? c[2]))?.nombre 
                   || `ID Act: ${c.actividad_id ?? c[2]}`,
        profesor: profesores.value.find(p => p.id == (c.profesor_id ?? c[3]))?.nombre 
                  || `ID Prof: ${c.profesor_id ?? c[3]}`,
        sala_nombre: salas.value.find(s => s.id == (c.sala_id ?? c[6]))?.nombre 
                  || `Sala ID: ${c.sala_id ?? c[6]}`, // Ensure this is sala_nombre
        // Comparamos el ID actual con el array de reservas
        yaReservada: clasesReservadasIds.value.includes(claseId), 
        imagen: 'https://images.unsplash.com/photo-1534438327276-14e5300c3a48?q=80&w=500'
      }
    })
  } catch (error) {
    console.error('Error al cargar clases:', error)
  }
}

onMounted(async () => {
  await fetchAuxData()
  await fetchClasesUsuario() // Obtenemos las reservas antes de renderizar la lista completa
  await fetchClases()
})

const abrirDialogCrear = () => {
  isEditing.value = false
  nuevaClase.value = { id_actividad: null, id_profesor: null, dia: '', hora: '08:00', id_sala: '', cupo_maximo: '' }
  horaSel.value = '08'
  dialog.value = true
}

const cerrarDialog = () => {
  dialog.value = false // Close the dialog
  nuevaClase.value = { id_actividad: null, id_profesor: null, dia: '', hora: '', id_sala: '', cupo_maximo: '' } // Reset form fields
  isEditing.value = false
}

const crearClase = async () => {
  try {
    const payload = {
      estado: 'Activa',
      id_actividad: nuevaClase.value.id_actividad,
      id_profesor: nuevaClase.value.id_profesor,
      id_sala: nuevaClase.value.id_sala,
      dia: nuevaClase.value.dia,
      hora: nuevaClase.value.hora,
      cupo_maximo: 1 // lo hardcodeo, despues lo vemos 
    }
    
    await ClasesService.publicarClase(payload)
    notificationStore.showNotification('La clase fue publicada con éxito', 'success')
    await fetchClases()
    cerrarDialog()
  } catch (error) {
    console.error('Error al publicar la clase:', error)
    const statusCode = error.response?.status;
    if (statusCode === 406 || statusCode === 407) {
      notificationStore.showNotification('Ya hay una clase en esa sala en ese horario', 'danger');
    } else if (statusCode === 408) {
      notificationStore.showNotification('La clase no se pudo publicar debido a que el cupo máximo elegido supera la capacidad que tiene la sala', 'danger');
    } else {
      // Mensaje genérico para otros errores
      notificationStore.showNotification('Hubo un error al publicar la clase', 'danger');
    }
  }
}

const actualizarClase = async () => {
  try {
    // Para editar, solo enviamos los campos que el backend permite modificar ahora
    const payload = {
      estado: 'Activa',
      id_profesor: nuevaClase.value.id_profesor,
      id_sala: nuevaClase.value.id_sala
    }
    
    await ClasesService.modificarClase(nuevaClase.value.id, payload)
    notificationStore.showNotification('Clase actualizada exitosamente', 'success')
    await fetchClases()
    cerrarDialog()
  } catch (error) {
    console.error('Error al actualizar clase:', error)
    notificationStore.showNotification('Hubo un error al actualizar la clase', 'danger')
  }
}

const editarClase = (clase) => {
  isEditing.value = true
  nuevaClase.value = { ...clase, id_sala: clase.sala } // Ensure id_sala is correctly populated
  dialog.value = true
}

const eliminarClase = async (clase) => {
  if (confirm(`¿Estás seguro de que deseas eliminar la clase de ${clase.categoria}?`)) {
    try {
      await ClasesService.eliminarClase(clase.id)
      notificationStore.showNotification('La clase fue eliminada con éxito', 'success')
      await fetchClases()
    } catch (error) {
      console.error('Error al eliminar clase:', error)
      const statusCode = error.response?.status;
      if (statusCode === 402 || statusCode === 403) {
        notificationStore.showNotification('No se puede eliminar una clase con usuarios inscriptos en alguna de sus instancias', 'danger');
      } else {
        notificationStore.showNotification('Hubo un error al eliminar la clase', 'danger')
      }
    }
  }
}

const cancelarClase = async (clase) => {
  if (confirm(`¿Estás seguro de que deseas marcar la clase de ${clase.categoria} como cancelada?`)) {
    try {
      await ClasesService.cancelarClase(clase.id)
      await fetchClases()
    } catch (error) {
      console.error('Error al cancelar clase:', error)
      notificationStore.showNotification('Hubo un error al cancelar la clase', 'danger')
    }
  }
}

const reservarClase = async (clase) => {
  try {
    const payload = {
      id_usuario: userProfile.value.id,
      fecha: clase.dia,
      hora: clase.hora,
    }
    
    const response = await ClasesService.reservarClase(clase.id, payload)
    
    // Recargamos el estado para actualizar los botones
    await fetchClasesUsuario()
    await fetchClases()
    if(response && response.status === 200){
      notificationStore.showNotification('Clase reservada exitosamente', 'success')
    } else if(response && response.status === 407){ {
      notificationStore.showNotification('El usuario ya posee una clase reservada para este horario', 'danger')   
    }}
    else{
      notificationStore.showNotification('No se pudo reservar la clase', 'danger')
    }

  } catch (error) {
    console.error('Error al reservar clase:', error)
    notificationStore.showNotification(error.message || 'Error al reservar clase', 'danger')
  }
}

const cancelarReserva = async (clase) => {
  try {
    // Asegúrate de usar el endpoint correcto de tu backend para cancelar
    // Por ejemplo: await ClasesService.cancelarReserva(clase.id, userProfile.value.id)
    console.log(`Ejecutando cancelación de la clase ${clase.id} para el usuario ${userProfile.value.id}`);
    
    // Aquí deberías colocar tu llamada a la API
    // await ClasesService.cancelarReserva(clase.id) 
    
    // Refrescamos los datos
    await fetchClasesUsuario()
    await fetchClases()
    
    notificationStore.showNotification('Reserva cancelada exitosamente', 'success')
  } catch (error) {
    console.error('Error al cancelar reserva:', error)
    notificationStore.showNotification('Hubo un error al cancelar la reserva', 'danger')
  }
}
</script>

<style scoped>
.classes-view {
  padding-top: 40px;
  background-color: var(--bg-main);
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