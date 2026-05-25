# Mapeo Frontend → Backend Python

## Adaptación de Servicios (Frontend Vue.js → Backend Python Flask)

### Cliente HTTP (`api.js`)
- Base URL: `http://127.0.0.1:5000`
- Métodos disponibles: `get()`, `post()`, `put()`, `patch()`, `delete()`
- Incluye automáticamente token de autorización desde localStorage
- Maneja errores y respuestas 2xx/4xx/5xx

### Rutas Mapeadas

#### 1. Autenticación
| Frontend (UsuariosServices.js) | Backend Python | Método | Status |
|---|---|---|---|
| `Usuarios/InicioSesion` | `/login` | POST | ✅ Implementado |
| `Usuarios/CerrarSesion` | (no existe) | POST | ⚠️ Mock local |

**Respuesta esperada de `/login`:**
```json
{
  "id": 1,
  "dni": 12345678,
  "nombre": "Juan",
  "apellido": "Pérez",
  "edad": 30,
  "telefono": "123",
  "correo": "juan.perez@example.com",
  "rol": "usuario",
  "genero": "masculino"
}
```

#### 2. Perfil de Usuario
| Frontend (UsuariosServices.js) | Backend Python | Método | Status |
|---|---|---|---|
| `Usuarios/VerPerfil` | `/usuarios/<id>/perfil` | GET | ✅ Implementado |
| `Usuarios/EditarUsuario/<userId>` | `/usuarios/<id>/perfil` | PUT | ✅ Implementado |
| `Usuarios/ObtenerAvatar/<userId>` | (no existe) | GET | ⚠️ Mock (null) |
| `Usuarios/SubirAvatar/<userId>` | (no existe) | POST | ⚠️ Mock |

**Datos esperados para actualizar perfil:**
```json
{
  "correo": "nuevo@example.com",
  "telefono": "987654321"
}
```

#### 3. Funcionalidades NO Implementadas en Backend
Las siguientes rutas retornan errores o son ignoradas:
- `Usuarios/CambiarContrasena/<userId>` ⚠️ No existe
- `Usuarios/RestablecerContrasena` ✅ Implementado
- `Usuarios/ConfirmarNuevaContrasena` ✅ Implementado
- `Usuarios/ObtenerListaUsuarios` ✅ Implementado

**Datos esperados para RestablecerContrasena perfil:**
```json
{
  "correo": "existente@example.com"
}
```

**Datos esperados para ConfirmarNuevaContrasena perfil:**
```json
{
  "correo": "existente@example.com",
  "nueva_contraseña": "12345678"
}
```

### Flujo de recuperacion de contraseña

1. **Usuario solicita restablecer contraseña**
   ```javascript
   restablecerContrasena({ correo: 'user@example.com' })
   → GET /usuarios/RestablecerContrasena
   → Se envía un correo electrónico al usuario
   ```

2. **Usuario accede al enlace recibido**
    - http://localhost:5173/ConfirmarNuevaContrasena?correo=user@example.com

3. **Frontend muestra formulario de nueva contraseña**

    Usuario ingresa:
    * nueva contraseña
    * confirmación de contraseña

    Se valida en frontend que ambas coincidan

4. **Usuario confirma nueva contraseña**
    ```javascript
    confirmarNuevaContrasena({
      correo: 'user@example.com',
      nueva_contraseña: 'NuevaPassword123'
    })
    → GET /usuarios/ConfirmarNuevaContrasena
    → Se actualiza la contraseña en la base de datos
    ```


### Flujo de Autenticación

1. **Usuario inicia sesión**
   ```javascript
   login({ correo: 'user@example.com', password: '1234' })
   → POST /login
   → Respuesta incluye ID y datos del usuario
   ```

2. **Estado se actualiza**
   - `_isLoggedIn` = true
   - `_userProfile` = datos del usuario
   - `_userRole` = rol del usuario

3. **Obtener perfil completo (opcional)**
   ```javascript
   fetchUserProfile() 
   → GET /usuarios/<id>/perfil
   → Obtiene información actualizada
   ```

4. **Actualizar perfil**
   ```javascript
   updateProfile({ correo: '...', telefono: '...' })
   → PUT /usuarios/<id>/perfil
   ```

### Cambios Realizados

**Frontend (`src/services/`):**
- ✅ Creado `api.js` - cliente HTTP basado en fetch
- ✅ Adaptado `UsuariosServices.js` - mapea rutas a endpoints Python
- ✅ Actualizado lógica de login para guardar ID de usuario
- ✅ Actualizado `fetchUserProfile()` para usar el ID almacenado

**Backend:**
- ✅ Sin cambios (rutas existentes mantenidas)

### Notas Importantes

1. El backend devuelve el ID del usuario en `/login`, que se usa para futuras peticiones
2. Las rutas con typo `/perfl` en la documentación del backend pueden ser un error
3. Funcionalidades de avatar, cambio de contraseña, etc., pueden agregarse al backend en el futuro
4. El cliente HTTP soporta token Bearer en header `Authorization` automáticamente
