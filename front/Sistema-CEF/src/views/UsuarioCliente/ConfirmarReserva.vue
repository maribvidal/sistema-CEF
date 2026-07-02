<template>
  <v-container class="py-10">
    <v-row justify="center">
      <v-col cols="12" md="8" lg="6">
        <v-card class="pa-6 text-center" rounded="lg" elevation="6">
          <v-card-title class="justify-center text-h5 font-weight-bold">
            {{ titulo }}
          </v-card-title>

          <v-card-text class="pt-3">
            <p class="text-body-1 mb-2">{{ descripcion }}</p>
            <p class="text-caption text-grey-darken-1">
              Usuario #{{ usuarioId }} · Clase #{{ claseId }} · Instancia #{{ instanciaId }}
            </p>

            <v-alert v-if="!usuarioId || !claseId || !instanciaId" type="warning" variant="tonal" class="mt-4">
              Faltan parámetros para confirmar la reserva.
            </v-alert>

            <div class="d-flex flex-wrap justify-center ga-3 mt-4">
              <v-btn
                v-if="!mostrarBotonMP"
                color="primary"
                @click="iniciarProcesoDePago"
                :loading="loading"
                :disabled="!usuarioId || !claseId || !instanciaId"
              >
                Generar Pago
              </v-btn>

              <v-btn variant="text" color="grey-darken-1" @click="emit('cancelar')">
                Cancelar
              </v-btn>
            </div>

            <div id="wallet_container" class="mt-4"></div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { computed, ref } from 'vue'
import { loadMercadoPago } from '@mercadopago/sdk-js'
import { PaymentsService } from '@/services/PaymentsService.js'
import { useNotificationStore } from '@/stores/notificationStore.js'

const props = defineProps({
  clase_id: {
    type: [String, Number],
    required: true,
  },
  inst_clase_id: {
    type: [String, Number],
    required: true,
  },
  usuario_id: {
    type: [String, Number],
    required: true,
  },
  tipo: {
    type: String,
    default: 'particular',
  },
})

const emit = defineEmits(['cancelar', 'confirmado'])

const notificationStore = useNotificationStore()

const loading = ref(false)
const mostrarBotonMP = ref(false)
const tipoReserva = computed(() => String(props.tipo ?? 'particular'))
const esMensualidad = computed(() => tipoReserva.value === 'mensualidad')

const usuarioId = computed(() => Number(props.usuario_id))
const claseId = computed(() => Number(props.clase_id))
const instanciaId = computed(() => Number(props.inst_clase_id))

const titulo = computed(() => (esMensualidad.value ? 'Confirmar Pago de Mensualidad' : 'Confirmar Pago de Clase'))
const descripcion = computed(() => (
  esMensualidad.value
    ? 'Genera el pago para tu reserva con mensualidad.'
    : 'Genera el pago para tu reserva particular.'
))

const iniciarProcesoDePago = async () => {
  loading.value = true
  
  try {
    const response = esMensualidad.value
      ? await PaymentsService.mothlyPayment(usuarioId.value, claseId.value)
      : await PaymentsService.oneTimePayment(usuarioId.value, instanciaId.value)

    const preferenceId =
      response?.data?.preference_id ??
      response?.data?.id ??
      response?.data?.data?.preference_id ??
      response?.data?.data?.id

    if (!preferenceId) {
      throw new Error('No se recibió un identificador de preferencia válido.')
    }

    await loadMercadoPago()

    const mp = new window.MercadoPago('APP_USR-07fa4e87-0b6c-4bd8-a671-6ffd56b5e362', {
      locale: 'es-AR'
    })

    mp.checkout({
      preference: {
        id: preferenceId
      },
      render: {
        container: '#wallet_container',
        label: 'Pagar con Mercado Pago',
      }
    })

    mostrarBotonMP.value = true
    notificationStore.showNotification('Pago generado correctamente.', 'success')
    emit('confirmado')

  } catch (error) {
    console.error('Error al inicializar Mercado Pago:', error)
    notificationStore.showNotification(
      error.response?.data?.message || error.message || 'No se pudo iniciar el pago.',
      'danger'
    )
  } finally {
    loading.value = false
  }
}
</script>