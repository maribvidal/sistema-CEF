<template>
  <v-container>
    <v-row justify="center">
      <v-col cols="12" md="10" lg="8">
        <v-card class="pa-6" elevation="4">
          <div class="text-h4 mb-2">Asistencias</div>
          <p class="text-body-1 text-medium-emphasis mb-6">
            Seleccioná una clase y luego registrá la asistencia por DNI o por QR.
          </p>

          <v-alert v-if="!claseSeleccionada" type="info" variant="tonal" class="mb-6">
            Primero elegí una clase para habilitar los botones.
          </v-alert>

          <v-select
            v-model="claseSeleccionada"
            :items="clasesDeLaSemana"
            item-title="titulo"
            item-value="id"
            label="Clase de la semana"
            variant="outlined"
            class="mb-6"
            clearable
          />

          <v-alert v-if="claseSeleccionada" type="success" variant="tonal" class="mb-6">
            Se usarán las instancias de la clase seleccionada para registrar la asistencia.
          </v-alert>

          <v-row>
            <v-col cols="12" md="6">
              <v-btn
                color="primary"
                block
                size="large"
                prepend-icon="mdi-card-account-details-outline"
                :disabled="!claseSeleccionada"
                @click="abrirDialogDni"
              >
                Pasar asistencia con DNI
              </v-btn>
            </v-col>
            <v-col cols="12" md="6">
              <v-btn
                color="secondary"
                block
                size="large"
                prepend-icon="mdi-qrcode-scan"
                :disabled="!claseSeleccionada"
                @click="abrirDialogQr"
              >
                Pasar asistencia con QR
              </v-btn>
            </v-col>
          </v-row>
        </v-card>
      </v-col>
    </v-row>

    <v-dialog v-model="dialogDni" max-width="420">
      <v-card>
        <v-card-title class="text-h6">Pasar asistencia con DNI</v-card-title>
        <v-card-text>
          <v-text-field
            v-model="dniIngresado"
            label="DNI"
            variant="outlined"
            type="text"
            autofocus
          />
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn variant="text" @click="cerrarDialogDni">Cancelar</v-btn>
          <v-btn color="primary" :disabled="!dniIngresado" @click="pasarAsistenciaDni">
            Confirmar
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-dialog v-model="dialogQr" max-width="420">
      <v-card>
        <v-card-title class="text-h6">Pasar asistencia con QR</v-card-title>
        <v-card-text>
          <p class="mb-0">
            Acá después podés conectar el lector QR o el componente de escaneo que prefieras.
          </p>
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn variant="text" @click="cerrarDialogQr">Cancelar</v-btn>
          <v-btn color="secondary" @click="pasarAsistenciaQr">
            Confirmar
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>


<script setup>
import { ref, onMounted } from 'vue'
import { ClasesService } from '@/services/ClasesServices.js'

const clasesDeLaSemana = ref([])
const claseSeleccionada = ref(null)
const profesores = ref([])
const salas = ref([])
const dialogDni = ref(false)
const dialogQr = ref(false)
const dniIngresado = ref('')

const obtenerRangoSemanaActual = () => {
  const inicio = new Date()
  inicio.setHours(0, 0, 0, 0)

  const diaActual = inicio.getDay()
  const desplazamientoInicio = diaActual === 0 ? -6 : 1 - diaActual
  inicio.setDate(inicio.getDate() + desplazamientoInicio)

  const fin = new Date(inicio)
  fin.setDate(inicio.getDate() + 6)
  fin.setHours(23, 59, 59, 999)

  return { inicio, fin }
}

const obtenerNombreActividad = (actividadId) => {
  switch (Number(actividadId)) {
    case 1:
      return 'Yoga'
    case 2:
      return 'Pilates'
    case 3:
      return 'Funcional'
    default:
      return `Actividad ${actividadId ?? 'desconocida'}`
  }
}

const formatearProfesores = (lista) => {
  if (!Array.isArray(lista)) return []
  return lista.map((profesor) => ({
    id: profesor.id ?? profesor[0],
    nombre: `${profesor?.nombre ?? profesor?.[2] ?? ''} ${profesor?.apellido ?? profesor?.[3] ?? ''}`.trim() || `Profesor ${profesor?.id ?? profesor?.[0]}`,
  }))
}

const formatearSalas = (lista) => {
  if (!Array.isArray(lista)) return []
  return lista.map((sala) => ({
    id: sala.id ?? sala[0],
    nombre: sala.nombre ?? sala[1] ?? `Sala ${sala.id ?? sala[0]}`
  }))
}

const obtenerNombreProfesor = (profesorId) => {
  return profesores.value.find((profesor) => profesor.id == profesorId)?.nombre ?? `Profesor ${profesorId ?? 'desconocido'}`
}

const obtenerNombreSala = (salaId) => {
  return salas.value.find((sala) => sala.id == salaId)?.nombre ?? `Sala ${salaId ?? 'desconocida'}`
}

const obtenerTituloClase = (instancia) => {
  return [
    obtenerNombreActividad(instancia.actividad_id),
    instancia.dia,
    instancia.hora,
    obtenerNombreSala(instancia.sala_id),
    obtenerNombreProfesor(instancia.profesor_id),
  ]
    .filter(Boolean)
    .join(' - ')
}

const cargarDatosAuxiliares = async () => {
  try {
    const [resProf, resSalas] = await Promise.all([
      ClasesService.listarProfesores(),
      ClasesService.listarSalas(),
    ])

    if (Array.isArray(resProf)) {
      profesores.value = formatearProfesores(resProf)
    }

    if (Array.isArray(resSalas)) {
      salas.value = formatearSalas(resSalas)
    }
  } catch (error) {
    console.error('Error al cargar profesores o salas:', error)
  }
}

const obtenerClasesDeLaSemana = async () => {
  try {
    const clasesTotales = await ClasesService.listarClases()
    console.log('Clases obtenidas:', clasesTotales)
    const listaClases = Array.isArray(clasesTotales) ? clasesTotales : []
    const { inicio, fin } = obtenerRangoSemanaActual()
    
    const clasesFiltradas = await Promise.all(
      listaClases.map(async (clase) => {
        try {
          const respuestaInstancias = await ClasesService.obtenerInstClaseSem(clase.id)
          const instanciaObtenida = respuestaInstancias?.data?.data
          const instancias = Array.isArray(instanciaObtenida)
            ? instanciaObtenida
            : instanciaObtenida
              ? [instanciaObtenida]
              : []

          const instanciasDeLaSemana = instancias.filter((instancia) => {
            const fechaInstancia = new Date(instancia.fecha)
            return fechaInstancia >= inicio && fechaInstancia <= fin
          })

          if (!instanciasDeLaSemana.length) return null

          const instancia = instanciasDeLaSemana[0]

          return {
            id: clase.id,
            nombre: obtenerNombreActividad(clase.actividad_id),
            actividad_id: clase.actividad_id,
            dia: clase.dia,
            hora: clase.hora,
            sala_id: clase.sala_id,
            profesor_id: clase.profesor_id,
            titulo: `${obtenerNombreActividad(clase.actividad_id)} | ${clase.dia} ${clase.hora} | ${obtenerNombreSala(clase.sala_id)} | ${obtenerNombreProfesor(clase.profesor_id)}`,
            instancias: instanciasDeLaSemana,
          }
        } catch (error) {
          console.error(`Error al procesar instancias para la clase ${clase.id}:`, error)
          return null
        }
      })
    )

    clasesDeLaSemana.value = clasesFiltradas.filter(Boolean)
  } catch (error) {
    console.error('Error al obtener las clases de la semana:', error)
  }


}

const abrirDialogDni = () => {
  dniIngresado.value = ''
  dialogDni.value = true
}

const cerrarDialogDni = () => {
  dialogDni.value = false
}

const abrirDialogQr = () => {
  dialogQr.value = true
}

const cerrarDialogQr = () => {
  dialogQr.value = false
}

const obtenerInstanciaSeleccionada = () => {
  const clase = clasesDeLaSemana.value.find((item) => item.id === claseSeleccionada.value)
  return clase?.instancias?.[0]?.id ?? null
}

const pasarAsistenciaQr = async () => {
  const inst_clase_id = obtenerInstanciaSeleccionada()

  if (!inst_clase_id) return

  try {
    console.log('Asistencia por QR lista para conectar', { inst_clase_id })
    cerrarDialogQr()
  } catch (error) {
    console.error('Error al pasar asistencia por QR:', error)
  }
}

const pasarAsistenciaDni = async () => {
  const inst_clase_id = obtenerInstanciaSeleccionada()
  const dni = dniIngresado.value.trim()

  if (!inst_clase_id || !dni) return

  try {
    await ClasesService.confirmarAsistenciaDNI(inst_clase_id, dni)
    console.log('Asistencia por DNI lista para conectar', { inst_clase_id, dni })
    cerrarDialogDni()
  } catch (error) {
    console.error('Error al pasar asistencia por DNI:', error)
  }
}

onMounted(() => {
  cargarDatosAuxiliares().then(() => {
    obtenerClasesDeLaSemana()
  })
})
</script>
