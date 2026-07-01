import apiClient from './api.js'

export const PaymentsService = {
    getPayments: async () => {
        return apiClient.get('/pagos')
    },

    getUserPayments: async (usuario_id) => {
        return apiClient.get(`/usuarios/${usuario_id}/pagos`)
    },

    getQRForPayment: async () => {
        return apiClient.get(`/pagos/obtenerQR`)
    },

    mothlyPayment: async (usuario_id, clase_id) => {
        return apiClient.post(`/mensualidad/pagar_mensualidad`, {
            usuario_id : usuario_id,
            clase_id: clase_id
        })
    },

    renewMembership: async (dni_cliente, descripcion ,id_mensualidad) => {
        return apiClient.post(`/mensualidad/renovar_mensualidad`, {
            dni_cliente: dni_cliente,
            descripcion: descripcion,
            id_mensualidad: id_mensualidad
        })
    },

    oneTimePayment: async (usuario_id, instancia_clase_id) => {
        return apiClient.post(`/reservas/individual/${usuario_id}/${instancia_clase_id}`)
    },
    agregarListaEsperaIndividual: async (usuario_id, instancia_clase_id) => {
        return apiClient.post(`/reservas/individual/${usuario_id}/${instancia_clase_id}/confirmar`, {})
    },
    
    agregarListaEsperaAbonados: async (dni_usuario, clase_id) => {
        return apiClient.post(`/reservas/abonado/${dni_usuario}/${clase_id}/confirmar`, {})
    },    getEstadoMensualidad: async (dni_cliente, id_mensualidad) => {
    const response = await apiClient.get('/mensualidad/ver_estado', { 
        params: { dni_cliente, id_mensualidad } //id_mensualidad mediante Query params
    })
    return response.data
    },

    cancelarMensualidad: async (dni_cliente, id_mensualidad) => {
        return apiClient.post(`/mensualidad/cancelar_mensualidad`, {
            dni_cliente: dni_cliente,
            id_mensualidad: id_mensualidad
        })
    },

    getMensualidadUsuario: async (dni_usuario) => {
        const response = await apiClient.get('/mensualidad/ver_mensualidades_usuario', {
            params: { dni_usuario }
        })
        return response.data
    },

    confirmarReservaIndividual: async (usuario_id, inst_clase_id) => {
        return apiClient.post(`/reservas/individual/${usuario_id}/${inst_clase_id}/confirmar`)
    },
    
    confirmarReservaAbonado: async (usuario_id, clase_id) => {
        return apiClient.post(`/reservas/abonado/${usuario_id}/${clase_id}/confirmar`)
    },

    cancelarReservaIndividual: async (reserva_id) => {
        return apiClient.delete(`/reservas/${reserva_id}/cancelar`)
    },

    obtenerReservasUsuario: async (usuario_id, inst_clase) => {
        return apiClient.get(`/usuarios/${usuario_id}/${inst_clase}/reserva`)
    },
}