# Documentación backend

## API

### Servidor

El servidor se va a abrir en la dirección **http://127.0.0.1:5000**

### Endpoints

Autenticación

| **Dirección** | **Método** | **Datos necesarios** | **Códigos de respuesta** |
| --- | --- | --- | --- |
| /login | POST | correo, contraseña | 404: Usuario no registrado |
|  |  |  | 400: Contraseña incorrecta |
|  |  |  | 200: Inicio de sesión exitoso. Se devuelve junto con la información de la cuenta, ya sea un usuario o un empleado |

Clases

| **Dirección** | **Método** | **Datos necesarios** | **Códigos de respuesta** |
| --- | --- | --- | --- |
| /clases | GET | - | 404: No se encontraron clases |
|  |  |  | 200: Se devuelve una lista de tuplas que representan clases. |

Empleados

| **Dirección** | **Método** | **Datos necesarios** | **Códigos de respuesta** |
| --- | --- | --- | --- |
| /empleados | GET | - | 404: No se encontraron clases |
|  |  |  | 200: Se devuelve una lista de los empleados con su información. |
| /empleados/(dni)/rol | PUT | Id del nuevo rol | 400: El id del rol es obligatorio; El empleado ya posee dicho rol |
|  |  |  | 404: El empleado no fue encontrado; El rol es inexistente |
|  |  |  | 200: Rol actualizado correctamente |

Usuarios

| **Dirección** | **Método** | **Datos necesarios** | **Códigos de respuesta** |
| --- | --- | --- | --- |
| /usuarios | POST | dni, nombre,
apellido, contraseña, correo, telefono, genero, edad | 400: El DNI ya se encuentra registrado; El correo electrónico ya se encuentra registrado; El usuario debe ser mayor de 14 años; Errores de validación de input |
|  |  |  | 201: Usuario registrado exitosamente |
| /usuarios/(id_usuario)/pagos | GET | Id del nuevo rol | 404: Usuario no encontrado; No se encontraron pagos para este usuario |
|  |  |  | 200: Se devuelven los pagos |
| /usuarios/(id_usuario)/perfil | PUT | correo, teléfono | 404: Usuario no encontrado |
|  |  |  | 400: Errores de validación de input; El correo electrónico ya se encuentra registrado por otro usuario |
|  |  |  | 200: Perfil actualizado exitosamente |
| /usuarios/(id_usuario)/perfl | GET |  | 404: Usuario no encontrado |
|  |  |  | 200: Se devuelve la información del perfil |

## Modelo lógico de la Base de Datos

## Testing

Para el testing se recomienda hacer archivos de Unit Test con la librería unittest de Python, y que estos archivos se guarden dentro de la carpeta **back/test_clases**. Esta librería provee una manera y un montón de funciones que permiten hacer el testing de la forma que lo haciamos en Java.
- Para ejecutar estos archivos, hay que correr en la terminal el siguiente comando: *python -m unittest <nombre_del_módulo_a_probar>*
- Se recomienda hacer los test cases por función.