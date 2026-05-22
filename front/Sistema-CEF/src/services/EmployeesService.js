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

  /**
   * Actualiza el rol de un empleado mediante su DNI
   * Endpoint: PUT /empleados/(dni)/rol
   */
  updateEmployeeRole: async (dni, roleId) => {
    const response = await apiClient.put(`/empleados/${dni}/rol`, { 
      rol_id: roleId 
    })
    return response.data
  }
}