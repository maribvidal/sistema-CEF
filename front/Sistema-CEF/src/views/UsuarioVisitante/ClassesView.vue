<template>
  <v-container class="classes-view" fluid>
    <v-row justify="center">
      <v-col cols="12" md="10">
        <h1 class="text-h4 mb-6 text-center font-weight-bold">Nuestras Clases</h1>

        <div 
          v-if="userRole === 1 || userRole === 2" 
          class="publish-clase-float d-flex justify-center justify-md-end"
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
  @click="abrirDialogReserva(clase)"
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
  @click="ejecutarCancelarReserva(clase)"
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

    <v-dialog v-model="checkoutDialog" max-width="500px" persistent>
      <v-card rounded="lg">
        <v-card-title class="pa-4 bg-black text-white">
          <span class="text-h5">Pagar con Mercado Pago</span>
        </v-card-title>

        <v-card-text>
          <div id="walletBrick_container"></div>
        </v-card-text>

        <v-card-actions>
          <v-spacer />
          <v-btn
            color="grey-darken-1"
            variant="text"
            @click="checkoutDialog = false"
          >
            Cancelar
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-dialog v-model="listaEsperaDialog" max-width="450px" persistent>
      <v-card rounded="lg">
        <v-card-title class="pa-4 bg-black text-white">
          <span class="text-h5">Sin cupo disponible</span>
        </v-card-title>
        <v-card-text class="pt-4">
          <p class="text-body-1 mb-4">
            No hay cupo disponible para la clase <strong>{{ claseParaReservar?.categoria }}</strong> en este horario.
          </p>
          <p class="text-body-2 text-grey-darken-1">
            ¿Deseas ingresar a la lista de espera? Te notificaremos cuando haya un lugar disponible.
          </p>
        </v-card-text>
        <v-divider></v-divider>
        <v-card-actions class="pa-4">
          <v-spacer></v-spacer>
          <v-btn 
            color="grey-darken-1" 
            variant="text" 
            @click="listaEsperaDialog = false"
            :disabled="ingresandoListaEspera"
          >
            Cancelar
          </v-btn>
          <v-btn 
            color="blue-darken-1" 
            variant="elevated" 
            @click="ingresarListaEspera"
            :loading="ingresandoListaEspera"
          >
            Inscribirse en lista de espera
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script setup>
import { ref, onMounted, watch, computed, nextTick } from 'vue'
import { loadMercadoPago } from '@mercadopago/sdk-js'
import { ClasesService } from '@/services/ClasesServices'
import { useRoute, useRouter } from 'vue-router'
// IMPORTANTE: Asegúrate de que UsuariosService exporte la función obtenerClase
import ConfirmarReserva from '@/views/UsuarioCliente/ConfirmarReserva.vue'

import { useNotificationStore } from '@/stores/notificationStore.js'
import { useAuth } from '@/services/UsuariosServices.js'
import { PaymentsService } from '@/services/PaymentsService.js'
const { userProfile, userRole } = useAuth()
const isEditing = ref(false)
const dialog = ref(false)
const notificationStore = useNotificationStore()
const reservaDialog = ref(false)
const confirmarReservaDialog = ref(false)
const pagoDialog = ref(false)
const claseParaReservar = ref(null)
const instanciaSeleccionada = ref(null)

const horas = Array.from({ length: 14 }, (_, i) => (i + 8).toString().padStart(2, '0'))
const horaSel = ref("08") // Valor por defecto para la hora seleccionada

const clasesReservadasIds = ref([]) // Estado para guardar las IDs de clases del usuario
const clasesReservadasInstancia = ref([]) // Track instance reservations locally
const tipoReserva = ref(null)
const cargandoPago = ref(false)
const checkoutDialog = ref(false)
const preferenceId = ref(null)
const listaEsperaDialog = ref(false)
const ingresandoListaEspera = ref(false)
watch(horaSel, (h) => {
  nuevaClase.value.hora = `${h}:00`
})

// PARA QUE SE REDIRIJA A LA PÁGINA SI EL PAGO FUE APROBADO - GEMINI
// Inicializamos las herramientas de enrutamiento
const route = useRoute()
const router = useRouter()

onMounted(() => {
  // 1. Revisamos si la URL trae el parámetro "collection_status" de Mercado Pago
  if (route.query.collection_status === 'approved') {
    
    // 2. Acá podés disparar tu notificación verde de éxito (como vi que tenés en tu sistema)
    // notificationStore.showNotification('¡Pago realizado con éxito!', 'success')
    alert("¡Pago procesado con éxito!") // (O usa tu propio sistema de alertas)
    alert(route.query.external_reference)
    // ACÁ LLAMAR AL ENDPOINT PARA APROBAR UN PAGO Y CREAR RESERVAS

    // 3. Redirigimos automáticamente a la página principal ('/')
    // Usamos .replace() en lugar de .push() para no dejar esa URL larga en el historial del navegador
    window.location.href = 'http://localhost:5173/clases'
  } 
  else if (route.query.collection_status === 'rejected' || route.query.collection_status === 'pending') {
    // También podés atajar si el pago falló o quedó pendiente
    alert("El pago no se pudo completar o está pendiente.")
    window.location.href = 'http://localhost:5173/clases'
  }
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
const diasSemana = ['Lunes', 'Martes', 'Miercoles', 'Jueves', 'Viernes', 'Sabado']

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


// Función que pide los datos al backend (seguramente ya tenés algo muy parecido)
const fetchClasesUsuario = async () => {
  if (userRole.value === 3 && userProfile.value?.id) {
    try {
      const response = await ClasesService.obtenerClase(userProfile.value.id)
      const misClases = response?.data?.data ?? response?.data ?? response

      if (Array.isArray(misClases)) {
        clasesReservadasIds.value = misClases.map(c => c.clase_id ?? c.id ?? c[0])
        console.log('IDs de clases reservadas:', clasesReservadasIds.value)
      } else {
        console.warn('No se pudo extraer un array de clases reservadas:', misClases)
        clasesReservadasIds.value = []
      }
    } catch (error) {
      console.error('Error al cargar clases del usuario:', error)
      if (error.status === 403) {
        clasesReservadasIds.value = []
        return
      }
      clasesReservadasIds.value = []
    }
  }
}

const comprobarClaseYaReservada = (claseId) => {
  return clasesReservadasIds.value.includes(claseId)
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
        yaReservada: comprobarClaseYaReservada(claseId),
        
        imagen: (() => {
          const nombre = actividades.value.find(a => a.id == (c.actividad_id ?? c[2]))?.nombre ?? '';
          if (nombre === 'Yoga') return 'https://images.unsplash.com/photo-1599901860904-17e6ed7083a0?q=80&w=500';
          if (nombre === 'Pilates') return 'https://plus.unsplash.com/premium_photo-1737321091046-ae81c7360cf0?q=80&w=1170&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D';
          return 'https://images.unsplash.com/photo-1534438327276-14e5300c3a48?q=80&w=500'; // Funcional por defecto
        })(),
        
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
  nuevaClase.value = { id_actividad: null, id_profesor: null, dia: '', hora: '08:00', id_sala: '', cupo_maximo: '', monto: '' }
  dialog.value = true
}

const cerrarDialog = () => {
  dialog.value = false
  nuevaClase.value = { id_actividad: null, id_profesor: null, dia: '', hora: '08:00', id_sala: '', cupo_maximo: '', monto: '' }
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
    if (statusCode === 409) {
      notificationStore.showNotification('Ya hay una clase en esa sala en ese horario', 'danger');
    } else if (statusCode === 408) {
      notificationStore.showNotification('La clase no se pudo publicar debido a que el cupo máximo elegido supera la capacidad que tiene la sala', 'danger');
    } else if (statusCode === 400) {
      notificationStore.showNotification('Este profesor no puede dar una clase de esa categoría', 'danger');
    } else if (statusCode === 411 || statusCode === 500) {
      notificationStore.showNotification('El profesor ya se encuentra ocupado en ese día y hora', 'danger');
    } else {
      // Mensaje genérico para otros errores
      notificationStore.showNotification('Hubo un error al publicar la clase', 'danger');
    }
  }
}

const actualizarClase = async () => {
  try {
    const montoViejo = clases.value.find(c => c.id === nuevaClase.value.id)?.monto
    console.log('Monto viejo:', montoViejo, 'Monto nuevo:', nuevaClase.value.monto)
    // Para editar, solo enviamos los campos que el backend permite modificar ahora
    const payload = {
      estado: 'Activa',
      id_profesor: nuevaClase.value.id_profesor,
      id_sala: nuevaClase.value.id_sala,
      monto: nuevaClase.value.monto
    }
    
    await ClasesService.modificarClase(nuevaClase.value.id, payload)
    if(montoViejo !== nuevaClase.value.monto) {
      notificationStore.showNotification('Clase actualizada exitosamente, el precio se modificará a partir del proximo mes', 'success')
    }
    else {
      notificationStore.showNotification('Clase actualizada exitosamente', 'success')
    }
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
  notificationStore.showNotification(
    `¿Estás seguro de que deseas eliminar la clase de ${clase.categoria}?`,
    'danger',
    0,
    async () => {
   {
    try {
      await ClasesService.eliminarClase(clase.id)
      notificationStore.showNotification('La clase fue eliminada con éxito', 'success')
      await fetchClases()
    } catch (error) {
      console.error('Error al eliminar clase:', error)
      const statusCode = error.status;
      if (statusCode === 402 || statusCode === 403 ) {
        notificationStore.showNotification('No se puede eliminar una clase con usuarios inscriptos en alguna de sus instancias', 'danger');
      }
      else if (statusCode === 404) {
        notificationStore.showNotification('No puede eliminar una clase con usuarios inscriptos en lista de espera', 'danger');
      }
      else {
        notificationStore.showNotification('Hubo un error al eliminar la clase', 'danger')
      }
    }
  }
},    0
  )
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


const hacerPagoMercadoPago = async () => {
  const clase = claseParaReservar.value
  if (!clase) return

  try {
    const response = await PaymentsService.mothlyPayment(
        userProfile.value.id,
        clase.id
      )
    
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
  const clase = claseParaReservar.value
  if (!clase || !userProfile.value?.id) return

  try {
    let responsePago

    if (tipoReserva.value === 'mensualidad') {
      responsePago = await PaymentsService.mothlyPayment(
        userProfile.value.id,
        clase.id
      )
    } else {
      const inst_clase = await ClasesService.obtenerInstClaseSem(clase.id)

      responsePago = await PaymentsService.oneTimePayment(
        userProfile.value.id,
        inst_clase.data.data.id
      )
    }
    console.log("Respuesta del backend para el pago:", responsePago)
    console.log("Preference ID recibido:", responsePago.data.preference_id)
    console.log("Datos adicionales:", responsePago.data)
    preferenceId.value = responsePago.data.preference_id

    checkoutDialog.value = true

    await renderCheckoutBrick()

  } catch (error) {
    console.error('Error detectado durante la transacción:', error)

    if (tipoReserva.value === 'particular' && error.status === 409) {
      checkoutDialog.value = false
      listaEsperaDialog.value = true
      return
    }

    if (tipoReserva.value === 'mensualidad' && error.status === 501) {
      checkoutDialog.value = false
      listaEsperaDialog.value = true
      return
    }

    const mensajeError =
      error.response?.data?.error ||
      error.response?.data?.message ||
      'No se pudo iniciar el pago.'

    notificationStore.showNotification(mensajeError, 'danger')

    checkoutDialog.value = false
    claseParaReservar.value = null
  }
}

const cerrarConfirmacionReserva = () => {
  confirmarReservaDialog.value = false
  instanciaSeleccionada.value = null
  claseParaReservar.value = null
  tipoReserva.value = null
}

const finalizarConfirmacionReserva = async () => {
  confirmarReservaDialog.value = false
  instanciaSeleccionada.value = null
  claseParaReservar.value = null
  await fetchClasesUsuario()
  await fetchClases()
  notificationStore.showNotification('Reserva confirmada exitosamente.', 'success')
}

// Ingresar a lista de espera cuando no hay cupo
const ingresarListaEspera = async () => {
  const clase = claseParaReservar.value
  if (!clase) return

  ingresandoListaEspera.value = true
  try {
    // Para mensualidades: usar endpoint de abonados
    if (tipoReserva.value === 'mensualidad') {
      const response = await PaymentsService.agregarListaEsperaAbonados(
        userProfile.value.id,
        clase.id
      )
    } else {
      // Para clases particulares: obtener instancia y usar endpoint individual
      const inst_clase = await ClasesService.obtenerInstClaseSem(clase.id)
      if (!inst_clase?.data?.data?.id) {
        throw new Error('No se pudo obtener la instancia de clase')
      }

      const response = await PaymentsService.agregarListaEsperaIndividual(
        userProfile.value.id, 
        inst_clase.data.data.id
      )
    }

    const tipo = tipoReserva.value === 'mensualidad' ? 'de abonados ' : ''
    notificationStore.showNotification(`¡Te has agregado a la lista de espera ${tipo}exitosamente!`, 'success')
    
    // Guardar localmente como reserva de instancia (para particulares)
    if (tipoReserva.value === 'particular' && clase.id && !clasesReservadasInstancia.value.includes(clase.id)) {
      clasesReservadasInstancia.value.push(clase.id)
    }
    
    // Cerrar diálogos y limpiar estado
    listaEsperaDialog.value = false
    claseParaReservar.value = null
    
    // Refrescar datos
    if (typeof fetchClasesUsuario === 'function') await fetchClasesUsuario()
    if (typeof fetchClases === 'function') await fetchClases()
  } catch (error) {
    console.error('Error al agregar a lista de espera:', error)
    const mensajeError = error.response?.data?.message || error.message || 'Error al agregar a la lista de espera'
    notificationStore.showNotification(mensajeError, 'danger')
  } finally {
    ingresandoListaEspera.value = false
  }
}

const renderCheckoutBrick = async () => {
  await loadMercadoPago()

  const mp = new MercadoPago(
    "APP_USR-3d8be2c7-4df5-4334-8582-5e848fa461eb"
  )

  const bricksBuilder = mp.bricks()

  await nextTick()

  await bricksBuilder.create(
    "wallet",
    "walletBrick_container",
    {
      initialization: {
        preferenceId: preferenceId.value
      }
    }
  )
}

// 1. Función para comprobar si el usuario ya está anotado en esta clase específica


// 2. Modificamos la función que abre el flujo de reserva para agregar el escudo de seguridad
const abrirDialogReserva = (clase) => {
  try {
    if (comprobarClaseYaReservada(clase.id)) {
      notificationStore.showNotification('Ya estás anotado en esta clase.', 'info')
      return
    }
    claseParaReservar.value = clase
    reservaDialog.value = true
  } catch (error) {
    console.error('Error al comprobar si la clase ya está reservada:', error)
    notificationStore.showNotification(error.message, 'danger')
    return
  }

  
}

// 3. Lógica para la cancelación (Ya tenías el borrador al final de tu archivo, la dejamos pulida)
const ejecutarCancelarReserva = async (clase) => {
  try {
    // Primero obtenemos la instancia de la semana para saber qué reserva cancelar
    const instancia = await ClasesService.obtenerInstClaseSem(clase.id)
    if (!instancia?.data?.data?.id) throw new Error('No se pudo obtener la instancia de clase para esta semana')
    const datos = await PaymentsService.obtenerReservasUsuario(userProfile.value.id, instancia.data.data.id)
    console.log('Datos de reserva obtenidos:', datos)
    console.log('ID de reserva a cancelar:', datos.data.data.id)
    await PaymentsService.cancelarReservaIndividual(datos.data.data.id)
    await fetchClasesUsuario()
    await fetchClases()
    notificationStore.showNotification('Reserva cancelada exitosamente.', 'success')
  } catch (error) {
    console.error('Error al cancelar reserva:', error)
    notificationStore.showNotification('Hubo un error al intentar cancelar la reserva.', 'danger')
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

.publish-clase-float {
  position: fixed;
  top: 88px;
  right: 24px;
  z-index: 20;
}

@media (max-width: 959px) {
  .publish-clase-float {
    top: auto;
    right: 16px;
    bottom: 16px;
    left: 16px;
  }

  .publish-clase-float :deep(.v-btn) {
    width: 100%;
  }
}
</style>

