import apiClient from './api.js'
import { ref, readonly } from 'vue'
import { createImageSrcFromBase64 } from './ImageFormatterService.js'

/**
 * ----------------------------------------------------------------
 * ESTADO REACTIVO DE AUTENTICACIÓN (SINGLETON)
 * ----------------------------------------------------------------
 * Estas variables mantienen el estado de la sesión del usuario en toda la aplicación.
 * Se exportan como 'readonly' para evitar modificaciones accidentales fuera de este servicio.
 */
const _isLoggedIn = ref(false)
const _userRole = ref(null)
const _userProfile = ref(null)

/**
 * ----------------------------------------------------------------
 * SERVICIO DE API DE AUTENTICACIÓN
 * ----------------------------------------------------------------
 * Un objeto privado que agrupa todas las llamadas directas a la API.
 * Esto separa la comunicación de red de la lógica de gestión de estado.
 */
const AuthApiService = {
  login: (credentials) => apiClient.post('Usuarios/InicioSesion', credentials),
  logout: () => apiClient.post('Usuarios/CerrarSesion'),
  getProfile: () => apiClient.get('Usuarios/VerPerfil'),
  getAvatar: (userId) => apiClient.get(`Usuarios/ObtenerAvatar/${userId}`),
  updateProfile: (userId, profileData) =>
    apiClient.patch(`Usuarios/EditarUsuario/${userId}`, profileData),
  uploadAvatar: (userId, avatarData) =>
    apiClient.post(`Usuarios/SubirAvatar/${userId}`, {
      Base64: avatarData.base64,
      Nombre: avatarData.nombre,
    }),
  changePass: (userId, passwords) =>
    apiClient.patch(`Usuarios/CambiarContrasena/${userId}`, passwords),
  restorePass: (requestData) =>
    apiClient.post('Usuarios/RestablecerContrasena', requestData),
  confirmNewPass: (token, newPassword) =>
    apiClient.post('Usuarios/ConfirmarNuevaContrasena', {
      Token: token,
      NuevaContrasena: newPassword,
    }),
  // ... Aquí se podrían mover otras llamadas a la API relacionadas con el usuario
}

export const AdminApiService = {
  userList: async () => {
    try {
      const response = await apiClient.get('/Usuarios/ObtenerListaUsuarios')
      return response.data
    } catch (error) {
      console.error('Error al obtener la lista de usuarios:', error)
      throw error
    }
  }
}

/**
 * ----------------------------------------------------------------
 * LÓGICA DE GESTIÓN DE ESTADO
 * ----------------------------------------------------------------
 */

/**
 * Limpia el estado de la sesión del usuario.
 */
const clearSession = () => {
  _isLoggedIn.value = false
  _userRole.value = null
  _userProfile.value = null
}

/**
 * Obtiene los datos del perfil y el avatar desde el backend y actualiza el estado global.
 * Esta es la única función que debe modificar el estado del perfil.
 * @param {boolean} force - Si es true, recarga los datos incluso si ya existen.
 */
const fetchUserProfile = async (force = false) => {
  if (_userProfile.value && !force) return

  try {
    const profileData = (await AuthApiService.getProfile()).data
    const avatarResponse = await AuthApiService.getAvatar(profileData.id).catch(() => null)

    const avatarUrl =
      avatarResponse && avatarResponse.data.base64
        ? createImageSrcFromBase64(avatarResponse.data.base64)
        : null

    _userProfile.value = { ...profileData, avatarUrl }
    _isLoggedIn.value = true
    _userRole.value = profileData.rol
  } catch (error) {
    // Si hay un error (ej. 401 Unauthorized por cookie inválida), limpiamos la sesión.
    console.error('No se pudo obtener el perfil de usuario, limpiando sesión.', error)
    clearSession()
  }
}

/**
 * ----------------------------------------------------------------
 * COMPOSABLE useAuth (INTERFAZ PÚBLICA)
 * ----------------------------------------------------------------
 * Agrupa el estado y las funciones que los componentes pueden usar.
 */
export const useAuth = () => {
  /**
   * Inicia sesión, establece la cookie y luego obtiene los datos del perfil.
   * @param {object} credentials - Objeto con email y password.
   */
  const login = async (credentials) => {
    await AuthApiService.login(credentials)
    // Después de un login exitoso, fetchUserProfile obtiene y establece todos los datos.
    await fetchUserProfile(true) // Forzamos la recarga.
    return _userProfile.value
  }

  /**
   * Cierra la sesión en el backend y limpia el estado local.
   */
  const logout = async () => {
    try {
      await AuthApiService.logout()
    } catch (error) {
      console.error('Error al cerrar la sesión en el backend:', error)
    } finally {
      clearSession()
    }
  }

  const changePassword = async (userId, passwords) => {
    await AuthApiService.changePass(userId, passwords)
  }

  const restorePassword = async (token, newPassword) => {
    await AuthApiService.restorePass(token, newPassword)
  }

  const confirmNewPassword = async (token, newPassword) => {
    await AuthApiService.confirmNewPass(token, newPassword)
  }


  return {
    // Estado (solo lectura para componentes)
    isLoggedIn: readonly(_isLoggedIn),
    userRole: readonly(_userRole),
    userProfile: readonly(_userProfile),

    // Acciones
    login,
    logout,
    fetchUserProfile,
    changePassword,
    restorePassword,
    confirmNewPassword,

    // También exponemos los métodos de la API para uso directo si es necesario
    // (ej. en vistas de edición de perfil).
    updateProfile: (profileData) => {
      if (!_userProfile.value) throw new Error('No hay sesión activa')
      // Incluimos el ID en el cuerpo de la petición también, por si el backend lo espera en el modelo.
      const payload = { ...profileData, id: _userProfile.value.id }
      return AuthApiService.updateProfile(_userProfile.value.id, payload)
    },
    uploadAvatar: (avatarData) => {
      if (!_userProfile.value) throw new Error('No hay sesión activa')
      return AuthApiService.uploadAvatar(_userProfile.value.id, avatarData)
    },
  }
}

// Para mantener la compatibilidad con el código existente que importa 'UsuariosService'
// y sus métodos directamente, se puede crear un objeto que simule la estructura anterior.
const UsuariosService = {
  actualizarPerfil: AuthApiService.updateProfile,
  subirAvatar: AuthApiService.uploadAvatar,
  // ... Añadir otros métodos si son importados directamente en otros archivos.
}
export default UsuariosService

/**
 * Configura los interceptores de Axios para manejar respuestas 401 (No autorizado).
 * Esto permite detectar cuándo el token ha expirado y cerrar la sesión automáticamente.
 * @param {Object} router - La instancia del router de Vue.
 */
export const setupAxiosInterceptors = (router) => {
  apiClient.interceptors.response.use(
    (response) => response,
    (error) => {
      if (error.response && error.response.status === 401) {
        console.warn('Sesión expirada o no autorizada (401). Cerrando sesión...')
        clearSession()

        // Redirigir al login si no estamos ya allí
        if (router && router.currentRoute.value.name !== 'inicioSesion') {
          router.push({ name: 'inicioSesion' })
        }
      }
      return Promise.reject(error)
    }
  )
}