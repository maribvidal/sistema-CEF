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

                  <div class="d-flex align-center mt-1" v-if="clase.monto > 0">
                    <v-icon size="small" class="mr-2" color="green-darken-2">mdi-cash</v-icon>
                    <span class="text-body-1 font-weight-bold">Precio:</span>
                    <span class="text-body-1 ml-2">${{ clase.monto }}</span>
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
                    @click="abrirDialogoReserva(clase)"
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
              <v-col cols="12" sm="6" v-if="!isEditing">
                <v-text-field
                  v-model.number="nuevaClase.cupo_maximo"
                  label="Cupo Máximo"
                  type="number"
                  min="0"
                  variant="outlined"
                  density="compact"
                  @update:modelValue="(value) => (nuevaClase.cupo_maximo = normalizarNoNegativo(value))"
                ></v-text-field>
              </v-col>
              <v-col cols="12" sm="6">
                <v-text-field
                  v-model.number="nuevaClase.monto"
                  label="Precio"
                  type="number"
                  min="0"
                  prefix="$"
                  variant="outlined"
                  density="compact"
                  @update:modelValue="(value) => (nuevaClase.monto = normalizarNoNegativo(value))"
                ></v-text-field>
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

    <v-dialog v-model="reservaDialog" max-width="500px" persistent>
      <v-card rounded="lg">
        <v-card-title class="pa-4 bg-black text-white">
          <span class="text-h5">Confirmar Reserva</span>
        </v-card-title>
        <v-card-text class="pt-4 text-body-1">
          ¿Cómo deseas reservar la clase de <strong>{{ claseParaReservar?.categoria }}</strong>?
        </v-card-text>
        <v-card-actions class="pa-4">
          <v-btn color="grey-darken-1" variant="text" @click="reservaDialog = false">Cancelar</v-btn>
          <v-spacer></v-spacer>
          <v-btn color="blue-darken-1" variant="elevated" @click="seleccionarTipoReserva('particular')">Clase Particular</v-btn>
          <v-btn color="green-darken-1" variant="elevated" @click="seleccionarTipoReserva('mensualidad')">Con Mensualidad</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-dialog v-model="qrDialog" max-width="450px" persistent>
      <v-card rounded="lg" class="text-center pb-4">
        <v-card-title class="pa-4 bg-black text-white mb-4">
          <span class="text-h5">Abonar con Mercado Pago</span>
        </v-card-title>
        
        <v-card-text>
          <div v-if="qrImage" class="d-flex justify-center">
            <v-img :src="qrImage" max-width="250" class="mb-4"></v-img>
          </div>
          <div v-else class="d-flex justify-center pa-8">
            <v-progress-circular indeterminate color="black" size="50"></v-progress-circular>
          </div>
          
          <p class="text-body-1 font-weight-bold mt-2 px-4">
            Escanea el código QR desde la app de Mercado Pago
          </p>
          <p class="text-caption text-grey-darken-1 px-6">
            Usa tu cuenta de prueba para abonar la modalidad de 
            <strong>{{ tipoReserva === 'particular' ? 'Clase Particular' : 'Mensualidad' }}</strong>.
          </p>
          
          <div class="d-flex justify-center align-center mt-6 text-blue-darken-2">
            <v-progress-circular indeterminate size="18" width="2" class="me-2"></v-progress-circular>
            <span class="text-body-2 font-weight-medium">Esperando confirmación del pago en tiempo real...</span>
          </div>
        </v-card-text>

        <v-card-actions class="justify-center mt-2">
          <v-btn color="grey-darken-2" variant="text" @click="cancelarFlujoPago">
            Cancelar Operación
          </v-btn>
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
import { PaymentsService } from '@/services/PaymentsService.js'
const { userProfile, userRole } = useAuth()
const isEditing = ref(false)
const dialog = ref(false)
const notificationStore = useNotificationStore()
const reservaDialog = ref(false)
const pagoDialog = ref(false)
const claseParaReservar = ref(null)

const horas = Array.from({ length: 14 }, (_, i) => (i + 8).toString().padStart(2, '0'))
const horaSel = ref(null)

const clasesReservadasIds = ref([]) // Estado para guardar las IDs de clases del usuario
const tipoReserva = ref(null)
const cargandoPago = ref(false)
const qrDialog = ref(false)
const qrImage = ref(null)
watch(horaSel, (h) => {
  nuevaClase.value.hora = `${h}:00`
})

const nuevaClase = ref({
  id_actividad: null,
  id_profesor: null,
  id_sala: '', 
  dia: '',
  hora: '',
  cupo_maximo: '',
  monto: ''
})

const clases = ref([])
const actividades = ref([])
const profesores = ref([])
const salas = ref([])
const diasSemana = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado']

const normalizarNoNegativo = (value) => {
  if (value === '' || value === null || value === undefined) return ''

  const numero = Number(value)
  if (!Number.isFinite(numero)) return ''

  return Math.max(0, numero)
}

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
const clasesUsuario = ref([])

// Función que pide los datos al backend (seguramente ya tenés algo muy parecido)
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
        monto: c.monto ?? c[8],
        categoria: actividades.value.find(a => a.id == (c.actividad_id ?? c[2]))?.nombre 
                   || `ID Act: ${c.actividad_id ?? c[2]}`,
        profesor: profesores.value.find(p => p.id == (c.profesor_id ?? c[3]))?.nombre 
                  || `ID Prof: ${c.profesor_id ?? c[3]}`,
        sala_nombre: salas.value.find(s => s.id == (c.sala_id ?? c[6]))?.nombre 
                  || `Sala ID: ${c.sala_id ?? c[6]}`, // Ensure this is sala_nombre
        // Comparamos el ID actual con el array de reservas
        yaReservada: clasesReservadasIds.value.includes(claseId), 
        imagen: (() => {
          const nombre = actividades.value.find(a => a.id == (c.actividad_id ?? c[2]))?.nombre ?? '';
          if (nombre === 'Yoga') return 'https://images.unsplash.com/photo-1599901860904-17e6ed7083a0?q=80&w=500';
          if (nombre === 'Pilates') return 'https://plus.unsplash.com/premium_photo-1737321091046-ae81c7360cf0?q=80&w=1170&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D';
          return 'https://images.unsplash.com/photo-1534438327276-14e5300c3a48?q=80&w=500'; // Funcional por defecto
        })()
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
  console.log('Clases del usuario:', clasesUsuario.value);
})

const abrirDialogCrear = () => {
  isEditing.value = false
  nuevaClase.value = { id_actividad: null, id_profesor: null, dia: '', hora: '', id_sala: '', cupo_maximo: '', monto: '' }
  dialog.value = true
}

const cerrarDialog = () => {
  dialog.value = false
  nuevaClase.value = { id_actividad: null, id_profesor: null, dia: '', hora: '', id_sala: '', cupo_maximo: '', monto: '' }
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
      cupo_maximo: nuevaClase.value.cupo_maximo,
      monto: nuevaClase.value.monto
    }
    
    await ClasesService.publicarClase(payload)
    notificationStore.showNotification('La clase fue publicada con éxito', 'success')
    await fetchClases()
    cerrarDialog()
  } catch (error) {
    console.error('Error al publicar la clase:', error)
    const statusCode = error.status
    if (statusCode === 406 || statusCode === 407) {
      notificationStore.showNotification('Ya hay una clase en esa sala en ese horario', 'danger');
    } else if (statusCode === 408) {
      notificationStore.showNotification('La clase no se pudo publicar debido a que el cupo máximo elegido supera la capacidad que tiene la sala', 'danger');
    } else if (statusCode === 400) {
      notificationStore.showNotification('Este profesor no puede dar una clase de esa categoría', 'danger');
    } else if (statusCode === 411) {
      notificationStore.showNotification('El profesor ya se encuentra ocupado en ese día y hora', 'danger');
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
      id_sala: nuevaClase.value.id_sala,
      monto: nuevaClase.value.monto
    }
    
    await ClasesService.modificarClase(nuevaClase.value.id, payload)
    notificationStore.showNotification('Clase actualizada exitosamente', 'success')
    await fetchClases()
    cerrarDialog()
  } catch (error) {
    const statusCode = error.status
    console.error('Error al actualizar clase:', error)
    
    if (statusCode === 405) {
      notificationStore.showNotification('Esa sala está ocupada en ese horario y fecha', 'danger')
    } else if (statusCode === 411) {
      notificationStore.showNotification('Ese profesor ya tiene una clase asignada en ese día y horario', 'danger')
    } else if (statusCode === 412) {
      notificationStore.showNotification('El profesor no está habilitado para dar esa actividad', 'danger')
    } else if (statusCode === 408) {
      notificationStore.showNotification('La clase no se pudo modificar debido a que el cupo máximo elegido supera la capacidad que tiene la sala', 'danger')
    } else {
      notificationStore.showNotification('Hubo un error al actualizar la clase', 'danger')
    }
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
      const statusCode = error.status;
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

const abrirDialogoReserva = (clase) => {
  claseParaReservar.value = clase
  reservaDialog.value = true
}

const hacerReserva = async (tipo) => {
  const clase = claseParaReservar.value
  if (!clase) return
  const inst_clase = await ClasesService.obtenerInstClaseSem(clase.id);
  if (!inst_clase) return

  // Aquí puedes diferenciar la lógica en el futuro
  console.log(`Iniciando reserva tipo: ${tipo} para la clase ${clase.id}`)

  try {
    const payload = {
      id_usuario: userProfile.value.id,
      fecha: clase.dia,
      hora: clase.hora,
    }

    const id_inst_clase = inst_clase.data.data.id

    const response = await ClasesService.reservarClase(id_inst_clase, payload)

    // Recargamos el estado para actualizar los botones
    await fetchClasesUsuario()
    await fetchClases()
    if (response && response.status === 200) {
      notificationStore.showNotification('Clase reservada exitosamente', 'success')
    } else if (response && response.status === 407) {
      notificationStore.showNotification('El usuario ya posee una clase reservada para este horario', 'danger')
    } else {
      notificationStore.showNotification('No se pudo reservar la clase', 'danger')
    }
  } catch (error) {
    console.error('Error al reservar clase:', error)
    notificationStore.showNotification(error.message || 'Error al reservar clase', 'danger')
  } finally {
    reservaDialog.value = false
    claseParaReservar.value = null
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

const hacerPagoMercadoPago = async () => {
  const clase = claseParaReservar.value
  if (!clase) return

  try {
    const response = await PaymentsService.mothlyPayment(clase.id, claseParaReservar.value.id)
    
    // Simulación de éxito
    notificationStore.showNotification('Redirigiendo a la pasarela de pago...', 'success')
  } catch (error) {
    console.error('Error al iniciar el pago:', error)
    notificationStore.showNotification('Hubo un error al iniciar el pago', 'danger')
  } finally {
    pagoDialog.value = false
    claseParaReservar.value = null
  }
}


const seleccionarTipoReserva = async (tipo) => {
  tipoReserva.value = tipo
  reservaDialog.value = false // Cierra el modal de selección de tipo
  
  // Dispara inmediatamente el flujo síncrono coordinado con tu backend
  await iniciarFlujoPagoCaja()
}

// Paso 2: Orquestación del flujo coordinado con el bucle síncrono del backend
const iniciarFlujoPagoCaja = async () => {
  const clase = claseParaReservar.value
  if (!clase) return

  try {
    // A. Primero traemos el QR fijo asignado a la caja (.env) para mostrarlo en pantalla
    const responseQr = await PaymentsService.getQRForPayment()
    let responseData = responseQr.data
    
    if (typeof responseData === 'string') {
      try {
        responseData = JSON.parse(responseData.replace(/'/g, '"'))
      } catch (e) {
        console.error('Error al deserializar respuesta de QR:', e)
      }
    }
    
    if (responseData && responseData.image) {
      qrImage.value = responseData.image
      qrDialog.value = true // Abrimos el modal: El usuario ya está viendo el QR en pantalla
    } else {
      throw new Error('No se pudo inicializar la imagen del código QR de la caja.')
    }

    // B. Con el QR ya renderizado, disparamos la petición de pago que ingresará al bucle 'while'
    const descripcion = `Pago QR de clase: ${clase.categoria}`
    let responsePago

    if (tipoReserva.value === 'mensualidad') {
      // Usamos el ID del perfil tal como requiere la clave foránea del backend
      responsePago = await PaymentsService.mothlyPayment(userProfile.value.id, clase.id)
    } else {
      // Pasamos los parámetros corregidos mapeando 'instancia_clase_id'
      responsePago = await PaymentsService.oneTimePayment(userProfile.value.id, descripcion, clase.id)
    }

    // C. Si el backend responde con éxito (Status 200), significa que salió del loop porque el usuario pagó
    notificationStore.showNotification('¡Pago verificado y reserva confirmada exitosamente!', 'success')
    
    // Refrescamos las vistas del usuario
    if (typeof fetchClasesUsuario === 'function') await fetchClasesUsuario()
    if (typeof fetchClases === 'function') await fetchClases()

    // Limpieza de estados y cierre automático del modal
    qrDialog.value = false
    claseParaReservar.value = null

  } catch (error) {
    console.error('Error detectado durante la transacción:', error)
    
    // Extraemos el mensaje de error nativo del back (como el mensaje de expiración 400)
    const mensajeError = error.response?.data?.error || error.response?.data?.message || 'La operación fue cancelada o expiró.'
    notificationStore.showNotification(mensajeError, 'danger')
    
    qrDialog.value = false
    claseParaReservar.value = null
  }
}

// Cancelación explícita desde el front
const cancelarFlujoPago = () => {
  qrDialog.value = false
  claseParaReservar.value = null
  notificationStore.showNotification('Transacción cancelada por el usuario.', 'info')
}

// 1. Función para comprobar si el usuario ya está anotado en esta clase específica
const yaTieneReserva = (claseId) => {
  // Si no hay datos, o si los datos no son un Array, devolvemos false automáticamente
  if (!clasesUsuario.value || !Array.isArray(clasesUsuario.value)) {
    return false;
  }
  console.log('Verificando si el usuario ya tiene reserva para la clase con ID:', claseId, 'Clases del usuario:', clasesUsuario.value);
  // Si es un array, procedemos a buscar
  return clasesUsuario.value.some(c => c.id === claseId || c.id_clase === claseId);
  
};

// 2. Modificamos la función que abre el flujo de reserva para agregar el escudo de seguridad
const abrirDialogReserva = (clase) => {
  // Si por alguna razón logra hacer click, el sistema lo frena acá
  if (yaTieneReserva(clase.id)) {
    notificationStore.showNotification('Ya posees una reserva activa para esta clase.', 'warning');
    return;
  }

  claseParaReservar.value = clase;
  reservaDialog.value = true;
};

// 3. Lógica para la cancelación (Ya tenías el borrador al final de tu archivo, la dejamos pulida)
const ejecutarCancelarReserva = async (clase) => {
  try {
    // Usamos el ID correspondiente para dar de baja la reserva
    await ClasesService.cancelarReserva(clase.id);
    
    // Refrescamos los datos inmediatamente para que los botones cambien en la pantalla
    await fetchClasesUsuario();
    await fetchClases();
    
    notificationStore.showNotification('Reserva cancelada exitosamente.', 'success');
  } catch (error) {
    console.error('Error al cancelar reserva:', error);
    notificationStore.showNotification('Hubo un error al intentar cancelar la reserva.', 'danger');
  }
};


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