import apiClient from './api.js'

export const ClasesService = {
  listarClases: async () => {
    const response = await apiClient.get('/clases')
    if (response.data?.status === 'success') {
      return response.data.data
    }
    // Si el backend envió status: "error", usamos su mensaje
    throw new Error(response.data?.message || 'Error en el servidor al obtener clases')
  },
  publicarClase: (clase) => apiClient.post('/clases', clase),
  modificarClase: (id, clase) => apiClient.put(`/clases/${id}`, clase),
  eliminarClase: (id) => apiClient.delete(`/clases/${id}`),
  cancelarClase: (id) => apiClient.patch(`/clases/${id}`),
  reservarClase: (id, payload) => apiClient.put(`/clases/${id}/reservar`, payload),
  obtenerClase: (idUser) => apiClient.get(`/usuarios/${idUser}/clases`),
  obtenerInstClaseSem: (id) => apiClient.get(`/clases/${id}/instancias/semana`),

  listarActividades: async () => {
    const response = await apiClient.get('/actividades')
    if (response.data?.status === 'success') {
      return response.data.data
    }
    throw new Error(response.data?.message || 'Error al obtener actividades')
  },
  listarProfesores: async () => {
    const response = await apiClient.get('/profesores')
    if (response.data?.status === 'success') {
      return response.data.data
    }
    throw new Error(response.data?.message || 'Error al obtener profesores')
  },
  listarSalas: async () => {
    const response = await apiClient.get('/salas')
    if (response.data?.status === 'success') {
      return response.data.data
    }
    throw new Error(response.data?.message || 'Error al obtener salas')
  },

  confirmarAsistenciaQR: async (inst_clase_id) => {
    const response = await apiClient.post(`/clientes/${inst_clase_id}/validar_qr`)
    return response.data
  },

  confirmarAsistenciaDNI: async (inst_clase_id, usuario_dni) => {
    const response = await apiClient.post(`/clientes/${inst_clase_id}/validar_dni/`, {
      usuario_dni
    })
   
    return response.data
  }
}
