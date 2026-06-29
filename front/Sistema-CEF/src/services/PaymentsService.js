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

    mothlyPayment: async (usuario_id, descripcion, id_mensualidad) => {
        return apiClient.post(`/pagos/mensualidad`, {
            usuario_id: usuario_id,
            descripcion: descripcion,
            id_mensualidad: id_mensualidad
        })
    },

    oneTimePayment: async (usuario_id, descripcion, clase_id) => {
        return apiClient.post(`/pagos/particular`, {
            usuario_id: usuario_id,
            descripcion: descripcion,
            clase_id: clase_id
        })
    }
}