export default {
  // Obtener token (encapsulado para poder migrar a cookie fácilmente)
  getToken() {
    try {
      return localStorage.getItem('token')
    } catch {
      return null
    }
  },

  // Guardar token
  setToken(token) {
    try {
      if (token) {
        localStorage.setItem('token', token)
      }
    } catch {
      // silenciar errores de almacenamiento
    }
  },

  // Eliminar token
  removeToken() {
    try {
      localStorage.removeItem('token')
    } catch {
      // silenciar errores de almacenamiento
    }
  },

  // Decodificar payload JWT (no verifica firma)
  getPayload() {
    try {
      const token = this.getToken()
      if (!token) return null
      const parts = token.split('.')
      if (parts.length !== 3) return null
      const base64 = parts[1].replace(/-/g, '+').replace(/_/g, '/')
      // Validar que el payload tenga formato base64 antes de decodificar
      if (!/^[A-Za-z0-9+/]+={0,2}$/.test(base64)) {
        console.error('TokenService.getPayload: payload JWT inválido (formato base64 incorrecto)')
        return null
      }
      const json = atob(base64)
      return JSON.parse(json)
    } catch (e) {
      console.error('TokenService.getPayload: error al decodificar el payload JWT:', e)
      return null
    }
  },

  // Comprobar expiración (retorna true si expirado o no hay token)
  isExpired() {
    const payload = this.getPayload()
    if (!payload || typeof payload.exp !== 'number') return true
    return payload.exp * 1000 < Date.now()
  },
}