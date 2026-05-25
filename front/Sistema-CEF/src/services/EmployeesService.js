import apiClient from './api.js'

export const EmployeesService = {
  /**
   * Obtiene la lista completa de empleados
   * Endpoint: GET /empleados
   */
  getEmployees: async () => {
    const response = await apiClient.get('/empleados')
    return response.data
  },
  getDisabledEmployees: async () => {
    const response = await apiClient.get('/empleados/desactivados')
    return response.data
  },
  getProfessors: async () => {
    const response = await apiClient.get('/profesores')
    return response.data
  },

  /**
   * Actualiza el rol de un empleado mediante su DNI
   * Endpoint: PUT /empleados/(dni)/rol
   */
  updateEmployeeRole: async (dni, roleId) => {
    const response = await apiClient.put(`/empleados/${dni}/rol`, { 
      rol_id: roleId 
    })
    return response.data
  },

  updateEmployeeInfo: async (dni, updatedData) => {
    const response = await apiClient.put(`/empleados/${dni}`, updatedData)
    return response.data
  }, // Aparentemente el endpoint es POST, aunque lo lógico sería un PUT o PATCH y falta implementar

  /**
   * Desactiva un empleado mediante su DNI
   * Endpoint: PATCH /empleados/(dni)/desactivar
   */
  deactivateEmployee: async (dni) => {
    const response = await apiClient.patch(`/empleados/${dni}/desactivar`)
    return response.data
  },

  /**
   * Crea un nuevo profesor
   */
  createProfessor: async (professorData) => {
    const response = await apiClient.post('/empleados', professorData)
    return response.data
  },

  /**
   * Crea un nuevo recepcionista (Usuario con rol 2)
   */
  createReceptionist: async (receptionistData) => {
    const response = await apiClient.post('/empleados', { ...receptionistData, rol: 2 })
    return response.data
  }
}