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
  }
}
