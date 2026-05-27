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
   * Nota: Se ajusta para usar el endpoint existente en el backend
   */
  updateEmployeeRole: async (dni, roleId) => {
    if (!dni) {
      console.error("Error: El DNI del empleado es undefined. Revisa el componente llamador.");
      throw new Error("DNI no proporcionado");
    }
    // El backend (empleados_route.py) maneja la actualización de rol 
    // Según documentación_backend.md: PUT /empleados/(dni)/rol
    const response = await apiClient.put(`/empleados/${dni}/${roleId}`, {     
    rol_id: parseInt(roleId) 
    })
    return response.data
  },

  updateEmployeeInfo: async (dni, updatedData) => {
    const response = await apiClient.put(`/empleados/${dni}`, updatedData)
    return response.data
  },

  /**
   * Elimina un empleado de forma logica mediante su DNI
   * Endpoint: DELETE /empleados/(dni)
   */
  deleteEmployee: async (dni) => {
    const response = await apiClient.delete(`/empleados/${dni}`)
    return response.data
  },

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
    const response = await apiClient.post('/empleados', { ...receptionistData, rol_id: 2 })
    return response.data
  }
}