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
    // El backend maneja la actualización a través del endpoint general de empleados
    const response = await apiClient.post(`/empleados/${dni}/permisos`, {     
      rol_id: parseInt(roleId) 
    })
    return response.data
  },

  updateEmployeeInfo: async (dni_viejo, dni_nuevo, data) => {
    console.log(data)
    const response = await apiClient.put(`/empleados/${dni_viejo}`, {
      nuevo_dni: dni_nuevo,
      nombre: data.nombre,
      apellido: data.apellido,
      correo: data.correo,
      genero: data.genero,
      rol_id: data.rol_id
    })
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
  createProfessor: async (data) => {
    const response = await apiClient.post('/profesores', {
      dni: data.dni,
      nombre: data.nombre,
      apellido: data.apellido,
      genero: data.genero
    })
    return response.data
  },

  /**
   * Crea un nuevo recepcionista (Usuario con rol 2)
   */
  createReceptionist: async (data) => {
    const response = await apiClient.post('/empleados/recepcionistas', {
      dni: data.dni,
      nombre: data.nombre,
      apellido: data.apellido,
      correo: data.correo,
      contraseña: data.contraseña,
      genero: data.genero
    })
    return response.data
  }
}