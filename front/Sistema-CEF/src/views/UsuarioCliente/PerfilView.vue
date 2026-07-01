<template>
  <v-container class="pa-6">
    <v-row justify="center">
      <v-col cols="12" md="8">
        <v-card elevation="6" class="pa-4">
          <v-row>
            <v-col cols="12" md="4" class="d-flex justify-center align-center">
              <v-avatar size="120">
                <v-img :src="avatarSrc" alt="Avatar" />
              </v-avatar>
            </v-col>

            <v-col cols="12" md="8">
              <div class="text-h5">{{ userName }} {{ lastName }}</div>
              <div class="text-subtitle-1 text--secondary">{{ userEmail }}</div>
              <div class="text-subtitle-1 text--secondary">Fecha de nacimiento: <strong>{{ userBirthDate }}</strong></div>
              <div class="mt-3">Rol: <strong>{{ rolUser }}</strong></div>

              <v-row class="mt-6" align="center" v-if="isOwnProfile">
                <v-col cols="12" sm="6">
                  <v-btn color="primary" block @click="goToEdit">Gestionar perfil</v-btn>
                </v-col>
                <v-col cols="12" sm="6">
                  <v-btn color="error" block variant="flat" @click="goToChangePassword">Cambiar contraseña</v-btn>
                </v-col>
                <v-row v-if="userProfile?.rol === 3 || userRole === 3">
                  <v-col cols="12" sm="6">
                    <v-btn color="secondary" block variant="flat" @click="handleGenerateQR">Generar QR</v-btn>
                  </v-col>
                  <v-col cols="12" sm="6">
                    <v-btn color="success" block variant="flat" @click="showPayments">Ver Pagos</v-btn>
                  </v-col>
                  <v-col cols="12" sm="6">
                    <v-btn color="primary" block variant="flat" @click="showMembershipStatus">Ver Estado de Mensualidad</v-btn>
                  </v-col>
              </v-row>
              </v-row>
            </v-col>
          </v-row>
        </v-card>
      </v-col>
    </v-row>
    <v-dialog v-model="dialogQR" max-width="400px">
      <v-card>
        <v-card-title class="text-h5">Código QR</v-card-title>
        <v-card-text>
          <div class="d-flex justify-center">
            <v-img :src="qrSrc" alt="QR Code" max-width="300" />
          </div>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn text @click="dialogQR = false">Cerrar</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <v-dialog v-model="dialogPayments" max-width="600px">
      <v-card>
        <v-card-title class="text-h5 d-flex align-center justify-space-between ga-3">
          <span>Historial de Pagos</span>
          <v-chip v-if="pagosSeleccionados.length" color="amber-darken-2" variant="tonal" label>
            {{ pagosSeleccionados.length }} seleccionados
          </v-chip>
        </v-card-title>
        <v-card-text>
          <v-alert
            v-if="payments.length"
            type="info"
            variant="tonal"
            class="mb-4"
          >
            Marca uno o más pagos para habilitar el botón de Mercado Pago.
          </v-alert>
          <v-table>
            <thead>
              <tr>
                <th class="text-left" style="width: 48px;"></th>
                <th class="text-left">Actividad</th>
                <th class="text-left">Fecha</th>
                <th class="text-left">Monto</th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="(payment, index) in payments"
                :key="payment?.id ?? `${payment?.fecha ?? 'payment'}-${index}`"
                v-if="payments?.length"
                :class="{ 'bg-amber-lighten-5': selectedPaymentIndexes.includes(index) }"
              >
                <td>
                  <v-checkbox-btn
                    v-model="selectedPaymentIndexes"
                    :value="index"
                    density="compact"
                    color="amber-darken-2"
                    :disabled="!esPagable(payment)"
                  />
                </td>
                <td>{{ payment.actividad_nombre }}</td>
                <td>{{ formatSpanishDate(payment.fecha) }}</td>
                <td>${{ payment.monto }}</td> 
                <td>
                  <v-chip
                    size="small"
                    :color="payment.estado === 'pending' ? 'amber-darken-2' : 'green-darken-1'"
                    variant="tonal"
                    label
                  >
                    {{ payment.estado }}
                  </v-chip>
                </td>
              </tr>
              <tr v-else>
               <td colspan="5" class="text-center">Sin pagos registrados.</td>
              </tr>
            </tbody>
          </v-table>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            v-if="pagosSeleccionados.length"
            color="amber-darken-2"
            variant="elevated"
            prepend-icon="mdi-credit-card-outline"
            :loading="cargandoPago"
            @click="pagarSeleccionados"
          >
            Pagar con Mercado Pago
          </v-btn>
          <v-btn
            v-if="pagosSeleccionados.length"
            variant="text"
            color="grey-darken-1"
            @click="limpiarSeleccionPagos"
          >
            Limpiar selección
          </v-btn>
          <v-btn text @click="dialogPayments = false">Cerrar</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <v-dialog v-model="checkoutDialog" max-width="560px" persistent>
      <v-card rounded="lg">
        <v-card-title class="pa-4 bg-black text-white">
          <span class="text-h5">Pagar con Mercado Pago</span>
        </v-card-title>
        <v-card-text class="pt-4">
          <p class="text-body-1 mb-2">
            Vas a pagar {{ pagosSeleccionados.length }} pago(s) por ${{ totalSeleccionado.toFixed(2) }}.
          </p>
          <div id="walletBrick_container"></div>
        </v-card-text>
        <v-card-actions class="pa-4">
          <v-spacer />
          <v-btn variant="text" color="grey-darken-1" @click="checkoutDialog = false">
            Cerrar
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <v-dialog v-model="dialogMembershipStatus" max-width="800px">
      <v-card>
        <v-card-title class="text-h5">Estado de Mensualidad</v-card-title>
        <v-card-text>
          <v-table>
            <thead>
              <tr>
                <th class="text-left">ID</th>
                <th class="text-left">Fecha Inicio</th>
                <th class="text-left">Fecha Fin</th>
                <th class="text-left">Estado</th>
                <th class="text-left">Acción</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="mensualidad in membershipStatus?.mensualidades" :key="mensualidad.id">
                <td>{{ mensualidad.id }}</td>
                <td>{{ formatSpanishDate(mensualidad.fecha_ini) }}</td>
                <td>{{ formatSpanishDate(mensualidad.fecha_fin) }}</td>
                <td>{{ mensualidad.activa ? 'Activa' : 'Inactiva' }}</td>
                <td>
                  <v-btn v-if="mensualidad.activa !== 1" color="primary" @click="renewMembership(userDNI, mensualidad.id)">Renovar</v-btn>
                  <span v-else> - </span>
                </td>
              </tr>
            </tbody>
          </v-table>
          
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn text @click="dialogMembershipStatus = false">Cerrar</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script setup>
import { ref, computed, onMounted, nextTick } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { loadMercadoPago } from '@mercadopago/sdk-js'
import { useAuth } from '@/services/UsuariosServices.js'
import DateFormatterService from '@/services/DateFormatterService.js'
// 1. Importamos la nueva función unificada
import { getValidImageSrc } from '@/services/ImageFormatterService.js' 
import defaultLogo from '@/assets/logoLargo.png'
import UsuariosService from '@/services/UsuariosServices.js'
import { PaymentsService } from '@/services/PaymentsService.js'
import { useNotificationStore } from '@/stores/notificationStore.js'


const notificationStore = useNotificationStore()

const router = useRouter()
const route = useRoute()
const { logout, fetchUserProfileById, userProfile: currentUser } = useAuth()
const { formatSpanishDate } = DateFormatterService

const profileData = ref(null)
// 2. avatarSrc ahora es un ref, inicializado con el logo por defecto
const avatarSrc = ref(defaultLogo) 
const userRole = computed(() => profileData.value?.rol_id || currentUser.value?.rol)

const getProfile = async () => {
  try {
    const profile = await fetchUserProfileById(route.params.id)
    profileData.value = profile
    
    // 3. Procesamos la imagen de forma asíncrona usando nuestro servicio inteligente
    if (profile?.avatarUrl) {
      const srcProcessado = await getValidImageSrc(profile.avatarUrl)
      if (srcProcessado) avatarSrc.value = srcProcessado
    }
  } catch (error) {
    console.error('Error fetching profile:', error)
  }
}

onMounted(() => {
  getProfile()
})

const rolUser = computed(() => {
  if(profileData.value?.rol_id) {
    switch(profileData.value.rol_id) {
      case 1: return 'Administrador'
      case 2: return 'Recepcionista'
      case 3: return 'Cliente'
      default: return 'Desconocido'
    }
  } else {
    return profileData.value?.tipo || 'Visitante'
  }
})

const userName = computed(() => profileData.value?.nombre || 'Usuario')
const lastName = computed(() => profileData.value?.apellido || '')
const userEmail = computed(() => profileData.value?.correo || '')
const userBirthDate = computed(() => formatSpanishDate(profileData.value?.fecha_nac))
const userDNI = computed(() => profileData.value?.dni || '')
const isOwnProfile = computed(() => currentUser.value?.id == route.params.id)

const onLogout = async () => {
  await logout()
  router.push('/inicioSesion')
}

const goToEdit = () => {
  router.push(`/editarPerfil/${route.params.id}`)
}

const goToChangePassword = () => {
  router.push(`/cambiarContraseña/${route.params.id}`)
}

const dialogQR = ref(false)
const qrSrc = ref(null)

// 1. Renombramos la función local (ej: handleGenerateQR o downloadQR)


const handleGenerateQR = async () => {
  try {
    
    const resultado = await UsuariosService.generarQR(route.params.id) 
    
    dialogQR.value = true

    
    if (resultado instanceof Blob) {
      
      const url = URL.createObjectURL(resultado)
      qrSrc.value = url
      
      setTimeout(() => URL.revokeObjectURL(url), 1000)
      
    } else if (resultado && typeof resultado === 'string') {
      
      console.log('Recibimos un string. Intentando abrir...')
      window.open(resultado, '_blank')
      
    } else if (resultado && typeof resultado === 'object') {
      
      console.log('Recibimos un JSON. Revisa las propiedades del objeto arriba.')
      
    } else {
      console.error('El formato recibido no es reconocido y no se puede crear el QR.')
    }

  } catch (error) {
    console.error('Error al generar el QR:', error)
  }
}

const dialogPayments = ref(false)
const payments   = ref([])
const selectedPaymentIndexes = ref([])
const cargandoPago = ref(false)
const checkoutDialog = ref(false)
const preferenceId = ref(null)

const pagosSeleccionados = computed(() =>
  selectedPaymentIndexes.value
    .map((index) => payments.value[index])
    .filter(Boolean)
)

const totalSeleccionado = computed(() =>
  pagosSeleccionados.value.reduce((total, payment) => total + Number(payment?.monto ?? 0), 0)
)

const limpiarSeleccionPagos = () => {
  selectedPaymentIndexes.value = []
}

const esPagable = (payment) => {
  return String(payment?.estado ?? '').toLowerCase() === 'pending'
}

const normalizarPagos = (payload) => {
  const lista = Array.isArray(payload)
    ? payload
    : Array.isArray(payload?.data)
      ? payload.data
      : Array.isArray(payload?.message)
        ? payload.message
        : []

  return lista.map((payment, index) => ({
    ...payment,
    __selectionId: payment?.id ?? `${payment?.fecha ?? 'payment'}-${index}`,
  }))
}

const showPayments = async () => {
  try {
    const result = await PaymentsService.getUserPayments(route.params.id)
    payments.value = normalizarPagos(result?.data ?? result)
    selectedPaymentIndexes.value = []

    if (!payments.value || payments.value.length === 0) {
      notificationStore.showNotification('Este usuario no tiene pagos asociados', 'danger')
      return
    }
    dialogPayments.value = true
  } catch (error) {
    notificationStore.showNotification('Este usuario no tiene pagos asociados', 'danger')
  }
}

const renderCheckoutBrick = async () => {
  await loadMercadoPago()

  const mp = new window.MercadoPago('APP_USR-07fa4e87-0b6c-4bd8-a671-6ffd56b5e362', {
    locale: 'es-AR'
  })

  const bricksBuilder = mp.bricks()
  await nextTick()

  await bricksBuilder.create('wallet', 'walletBrick_container', {
    initialization: {
      preferenceId: preferenceId.value,
    },
  })
}

const pagarSeleccionados = async () => {
  if (!pagosSeleccionados.value.length) return

  const idsSeleccionados = pagosSeleccionados.value
    .filter(esPagable)
    .map((payment) => payment.id)

  if (!idsSeleccionados.length) {
    notificationStore.showNotification('Sólo podés pagar pagos pendientes.', 'danger')
    return
  }

  cargandoPago.value = true
  try {
    const response = await PaymentsService.crearPreferenciaPagosSeleccionados(route.params.id, idsSeleccionados)
    preferenceId.value = response?.data?.preference_id || response?.data?.data?.id

    if (!preferenceId.value) {
      throw new Error('No se recibió una preferencia válida.')
    }

    checkoutDialog.value = true
    await renderCheckoutBrick()

    notificationStore.showNotification('Pago preparado correctamente.', 'success')
  } catch (error) {
    console.error('Error al preparar el pago:', error)
    notificationStore.showNotification(
      error.response?.data?.message || error.response?.data?.error || error.message || 'No se pudo iniciar el pago.',
      'danger'
    )
  } finally {
    cargandoPago.value = false
  }
}

const dialogMembershipStatus = ref(false)
const membershipStatus = ref(null)

const showMembershipStatus = async () => {
  try {
    const mensualidad = await PaymentsService.getMensualidadUsuario(userDNI.value)

    const mensualidades = mensualidad?.message ?? []
    if (!Array.isArray(mensualidades) || mensualidades.length === 0) {
      throw new Error('El usuario no posee mensualidades registradas.')
    }

    const mensualidadActiva = mensualidades.find(item => Number(item.estado) === 1) ?? mensualidades[0]
    membershipStatus.value = {
      activa: Number(mensualidadActiva.estado) === 1,
      fechaFin: mensualidadActiva.fecha_fin,
      fechaIni: mensualidadActiva.fecha_ini,
      id: mensualidadActiva.id,
      mensualidades
    }
    dialogMembershipStatus.value = true
  } catch (error) {
    notificationStore.showNotification('El usuario no posee mensualidades activas', 'danger')
  }
}

const renewMembership = async (userId, id_mensualidad) => {
  try {
    const response = await PaymentsService.renewMembership(userId, "desc",id_mensualidad)
    if (response && response.status === 200) {
      notificationStore.showNotification('Mensualidad renovada exitosamente.', 'success')
      showMembershipStatus()
    } else {
      throw new Error('Error al renovar la mensualidad.')
    }
  } catch (error) {
    console.error('Error al renovar la mensualidad:', error)
    notificationStore.showNotification('Error al renovar la mensualidad.', 'danger')
  }

}
</script>

<style scoped>
.text-h5 {
  font-weight: 600;
}
.text--secondary {
  color: var(--text-secondary);
}
</style>