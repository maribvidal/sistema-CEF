import apiClient from './api.js'
import { ref, readonly } from 'vue'
import { createImageSrcFromBase64 } from './ImageFormatterService.js'
import TokenService from './TokenService.js'

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
/**
 * Mapea las rutas esperadas por el frontend a las rutas del backend Python
 * Backend: http://127.0.0.1:5000
 */
const AuthApiService = {
  // Login: mapea Usuarios/InicioSesion → /login
  login: (credentials) => apiClient.post('/login', {
    correo: credentials.correo || credentials.email,
    contraseña: credentials.contraseña || credentials.password,
  }),

  // Logout: cierra sesión (endpoint no implementado en backend, usando mock)
  logout: async () => {
    // El backend no tiene endpoint de logout, solo limpiamos token localmente
    localStorage.removeItem('token')
    return { data: { mensaje: 'Sesión cerrada' }, status: 200 }
  },

  // GetProfile: mapea Usuarios/VerPerfil → /usuarios/<id>/perfil
  getProfile: (userId) => apiClient.get(`/usuarios/${userId}/perfil`),

  // GetAvatar: mapea Usuarios/ObtenerAvatar → No implementado en backend
  getAvatar: async (userId) => {
    const response = await apiClient.get(`/usuarios/${userId}/avatar`)
    return response.data
  },

  // UpdateProfile: mapea Usuarios/EditarUsuario → /usuarios/<id>/perfil PUT
  updateProfile: (userId, profileData) =>
    apiClient.put(`/usuarios/${userId}/perfil`, {
      correo: profileData.correo || profileData.email,
      telefono: profileData.telefono || profileData.phone,
      fecha_nac: profileData.fecha_nac || profileData.birthDate,
      // Incluir otros campos que el backend pueda esperar, como nombre, apellido, etc.
      nombre: profileData.nombre || profileData.name,
      apellido: profileData.apellido || profileData.lastName,
    }),

  // UploadAvatar: mapea Usuarios/SubirAvatar → No implementado en backend
  uploadAvatar: (userId, avatarData) => {
    return apiClient.post(`/usuarios/${userId}/avatar`, {
      avatar: avatarData.avatar || avatarData.base64 || avatarData
    })

  },

  // ChangePassword: mapea Usuarios/CambiarContrasena → No implementado en backend
  changePass: async (userId, passwords) => {
    apiClient.put(`/usuarios/${userId}/contraseña`, {
      contraseña_actual: passwords.currentPassword,
      nueva_contraseña: passwords.newPassword
    }
  )
  },

  // RestorePassword: mapea Usuarios/RestablecerContrasena → No implementado en backend
  restorePass: async (requestData) => {
    console.warn('restorePass no implementado en backend Python')
    throw new Error('Funcionalidad no disponible en este momento')
  },

  // ConfirmNewPassword: mapea Usuarios/ConfirmarNuevaContrasena → No implementado en backend
  confirmNewPass: async (token, newPassword) => {
    console.warn('confirmNewPass no implementado en backend Python')
    throw new Error('Funcionalidad no disponible en este momento')
  },
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
  TokenService.removeToken()
}

/**
 * Inicializa la autenticación desde el token guardado en localStorage.
 * Se debe llamar en main.js al cargar la aplicación.
 */
export const initAuth = () => {
  const token = TokenService.getToken()
  console.log('[initAuth] Token encontrado:', !!token)
  if (token) {
    const payload = TokenService.getPayload()
    console.log('[initAuth] Payload decodificado:', payload)
    if (payload) {
      // Restaurar el estado del usuario desde el payload del JWT
      _userProfile.value = {
        id: payload.id,
        dni: payload.dni,
        nombre: payload.nombre,
        tipo: payload.tipo,
        rol: payload.rol
      }
      _isLoggedIn.value = true
      _userRole.value = payload.rol || null
      console.log('[initAuth] Sesión restaurada:', { id: payload.id, nombre: payload.nombre })
    } else {
      // Token inválido o expirado
      console.log('[initAuth] Token inválido, limpiando sesión')
      clearSession()
    }
  } else {
    console.log('[initAuth] No hay token guardado')
  }
}

/**
 * ----------------------------------------------------------------
 * LÓGICA COMPARTIDA DE EXTRACCIÓN DE DATOS
 * ----------------------------------------------------------------
 */

/**
 * Encapsula la lógica repetitiva de consultar perfil y avatar de un usuario
 * para luego unificarlos en un solo objeto.
 * 
 * @param {string|number} userId - Identificador del usuario.
 * @returns {Promise<object>} Los datos unificados del perfil y la URL del avatar.
 */
const fetchAndFormatProfileData = async (userId) => {
  const profileResponse = await AuthApiService.getProfile(userId)
  const profileData = profileResponse.data.perfil || profileResponse.data

  const avatarResponse = await AuthApiService.getAvatar(userId).catch(() => null)
  const avatarBase64 = avatarResponse?.avatar || avatarResponse?.data?.avatar || avatarResponse?.data?.base64
  const avatarUrl = avatarBase64
    ? createImageSrcFromBase64(avatarBase64)
    : null

  return { ...profileData, avatarUrl }
}

/**
 * Obtiene los datos del perfil y el avatar desde el backend para el usuario en sesión
 * y actualiza el estado global. Esta es la única función que debe modificar el estado del perfil.
 * 
 * @param {boolean} force - Si es true, fuerza la recarga de los datos aunque ya existan.
 */
const fetchUserProfile = async (force = false) => {
  if (_userProfile.value && !force) return

  try {
    if (!_userProfile.value?.id) {
      throw new Error('No se puede obtener perfil: falta ID de usuario en sesión.')
    }

    const mergedProfileData = await fetchAndFormatProfileData(_userProfile.value.id)

    _userProfile.value = mergedProfileData
    _isLoggedIn.value = true
    _userRole.value = mergedProfileData.rol || _userRole.value

  } catch (error) {
    console.error('[fetchUserProfile] Falló la obtención del perfil local, limpiando estado.', error)
    clearSession()
  }
}

/**
 * Consulta un perfil aleatorio o arbitrario según su ID.
 * Útil para roles de admin que deseen ver otro perfil además del propio.
 * 
 * @param {string|number} userId - Identificador único del usuario a consultar.
 * @returns {Promise<object>} Objeto final con perfil y avatar.
 */
const fetchUserProfileById = async (userId) => {
  try {
    return await fetchAndFormatProfileData(userId)
  } catch (error) {
    console.error(`[fetchUserProfileById] Error al obtener el perfil del userId [${userId}]:`, error)
    throw error
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
   * Inicia sesión, establece el token en localStorage y luego obtiene los datos del perfil.
   * @param {object} credentials - Objeto con email y password.
   */
  const login = async (credentials) => {
    const response = await AuthApiService.login(credentials)
    
    console.log('[login] Respuesta del servidor:', response.data)
    
    // Guardar el token en localStorage
    if (response.data.token) {
      TokenService.setToken(response.data.token)
      console.log('[login] Token guardado en localStorage')
    }
    
    // Guardar la información del usuario devuelta por login
    // El backend devuelve la info del usuario en el endpoint /login
    _userProfile.value = response.data.usuario
    _isLoggedIn.value = true
    _userRole.value = response.data.usuario.rol || null
    
    console.log('[login] Estado actualizado:', { 
      isLoggedIn: _isLoggedIn.value,
      usuario: _userProfile.value 
    })
    
    // Opcionalmente, obtener información completa del perfil si es necesario
    // await fetchUserProfile(true)
    
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
    fetchUserProfileById,

    // También exponemos los métodos de la API para uso directo si es necesario
    // (ej. en vistas de edición de perfil).
    updateProfile: (profileData) => {
      if (!_userProfile.value) throw new Error('No hay sesión activa')
      // Incluimos el ID en el cuerpo de la petición también, por si el backend lo espera en el modelo.
      const payload = { ...profileData, id: _userProfile.value.id }
      // El backend requiere el ID en la URL (usuario_id)
      const identifier = _userProfile.value.id
      return AuthApiService.updateProfile(identifier, payload)
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