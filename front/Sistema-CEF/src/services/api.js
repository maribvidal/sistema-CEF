/**
 * Cliente HTTP para comunicarse con el backend Python
 * Base URL: http://127.0.0.1:5000
 */

const API_BASE_URL = 'http://127.0.0.1:5000'

/**
 * Realiza una petición HTTP genérica
 * @param {string} endpoint - La ruta del endpoint (ej: /login)
 * @param {string} method - GET, POST, PUT, PATCH, DELETE
 * @param {object} data - Datos a enviar en el cuerpo (opcional)
 * @returns {Promise} Respuesta del servidor
 */
async function request(endpoint, method = 'GET', data = null, params = null) {
  let url = `${API_BASE_URL}${endpoint}`
  if (params) {
    const query = new URLSearchParams(params).toString()
    url = `${url}?${query}`
  }
  const options = {
    method,
    headers: {
      'Content-Type': 'application/json',
    },
  }

  // Incluir token si existe
  const token = localStorage.getItem('token')
  if (token) {
    options.headers['Authorization'] = `Bearer ${token}`
  }

  // Agregar datos al cuerpo si existen
  if (data && (method === 'POST' || method === 'PUT' || method === 'PATCH')) {
    options.body = JSON.stringify(data)
  }

  try {
    const response = await fetch(url, options)

    // Parsear JSON de la respuesta
    let jsonData
    try {
      jsonData = await response.json()
    } catch {
      jsonData = null
    }

    // Si la respuesta no es 2xx, lanzar error
    if (!response.ok) {
      const error = new Error(
        jsonData?.message ||
        jsonData?.error ||
        (Array.isArray(jsonData) ? 'Errores de validación en los datos' : null) ||
        `HTTP ${response.status}`
      )

      error.status = response.status
      error.data = jsonData

      throw error
    }

    return {
      data: jsonData,
      status: response.status,
    }
  } catch (error) {
    console.error(`Error en ${method} ${url}:`, error)
    throw error
  }
}

/**
 * Cliente API con métodos auxiliares
 */
const apiClient = {
  get: (endpoint, options = {}) => request(endpoint, 'GET', null, options.params),
  post: (endpoint, data) => request(endpoint, 'POST', data),
  put: (endpoint, data) => request(endpoint, 'PUT', data),
  patch: (endpoint, data) => request(endpoint, 'PATCH', data),
  delete: (endpoint) => request(endpoint, 'DELETE'),
}

export default apiClient
