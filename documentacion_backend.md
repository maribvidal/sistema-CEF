# Documentación backend

## Roles

- 0: Desactivado
- 1: Administrador
- 2: Recepcionista
- 3: Usuario
- 4: Eliminado
- 5: Profesor

## API

### ¿Qué devuelven los endpoints?

Cualquier query que se haga a la Base de Datos devuelve lo siguiente, en caso de éxito o de error:

| **Query** | **Primer campo objeto** | **Segundo campo objeto** | **Código** |
| --- | --- | --- | --- |
| **Éxito** | *status* | *data* | 200 |
| **Error** | *status* | *message* | 40X, 500 |
- El campo *status* puede devolver dos valores: “success” o “error”
- Si *status* es “success”, entonces el segundo campo es *data*, por el cual se devuelve un resultado
    - Si la query es una **consulta de una tupla**, se devuelve un objeto **dict** con la información.
    - Si la query son múltiples consultas de tuplas, se devuelve un objeto dict con toda la información.
    - Si la query es de **inserción**, se devuelve un valor tipo entero que representa el **id insertado**.
    - Si la query es de **otro tipo**, se devuelve **None**.
- Si *status* es “error”, entonces el segundo campo es *message*, por el cual se devuelve el mensaje de error que emitió el programa.

### Servidor

El servidor se va a abrir en la dirección **http://127.0.0.1:5000**

### Endpoints

Autenticación

| **Dirección** | **Método** | **Datos necesarios** | **Códigos de respuesta** |
| --- | --- | --- | --- |
| /login | POST | correo, contraseña | 400: Contraseña o datos incorrectos <br> 500: Error interno de base de datos o consulta <br> 200: Inicio de sesión exitoso. Se devuelve junto con el token JWT y la información de la cuenta. |
| /registro | POST | dni, nombre, apellido, contraseña, fecha_nac, correo, telefono, genero, rol | 400: Errores lógicos de validación de inputs generales <br> 401: El rol_id proporcionado no es válido <br> 402: La fecha de nacimiento no cuenta con un formato válido (%Y-%m-%d) <br> 403: El usuario debe ser mayor de 14 años <br> 404: Error al obtener los DNIs de los usuarios <br> 405: El DNI ya se encuentra registrado para un usuario común <br> 406: Error al validar el correo electrónico <br> 500: Error del lado del servidor al intentar insertar <br> 200: Usuario registrado exitosamente. |
| /clientes/(id_cliente)/qr | GET | - | 200: Se devuelve la imagen del código QR autogenerado en formato PNG. |
| /clientes/(inst_clase_id)/validar_qr | POST | id_usuario | 404: No se encontró una reserva para ese cliente en esa clase <br> 500: Error de servidor al consultar reservas <br> 200: Asistencia confirmada exitosamente. |

Clases

| **Dirección** | **Método** | **Datos necesarios** | **Códigos de respuesta** |
| --- | --- | --- | --- |
| /clases | GET | - | 400: Error interno de consulta <br> 401: No se encontraron clases <br> 200: Se devuelve la lista de clases disponibles. |
| /clase | GET | - | 400: Error interno de consulta <br> 401: No se encontraron clases <br> 200: Se devuelve la lista de clases sin información extra de ocurrencia. |
| /clases | POST | estado, id_actividad, id_profesor, id_sala, dia, hora, cupo_maximo, (opcional: primera_fecha) | 400/401: Error o Actividad no encontrada <br> 402/403: Error o Profesor no encontrado <br> 404/405: Error o Sala no encontrada <br> 406/407: Error o la Sala ya se encuentra ocupada <br> 408: El cupo máximo supera la capacidad de la sala <br> 410/411: Error de servidor o la clase ya estaba insertada <br> 412: La fecha no coincide con el día <br> 413: Formato de fecha inválido <br> 414/415: Error al insertar listas de espera <br> 416/417: Error al insertar instancia de clase <br> 418/419: Error al crear lista de espera individual <br> 200: Clase publicada exitosamente. |
| /clases/(id_clase) | PUT | estado, id_sala | 400: Faltan campos o Error interno de consulta <br> 401: Clase no encontrada <br> 402/403: No se puede modificar (ya tiene instancia asociada) <br> 404: Error de base de datos al modificar <br> 200: Clase modificada exitosamente. |
| /clases/(id_clase) | DELETE | - | 400: Error interno <br> 401: Clase no encontrada <br> 402/403: No se puede eliminar (tiene instancia asociada) <br> 404: Error en base de datos al eliminar <br> 200: Clase eliminada exitosamente. |
| /clases/(id_clase) | PATCH | - | 400: Error de consulta <br> 401: Clase no encontrada <br> 402/403: No se puede cancelar (tiene instancia asociada) <br> 404: Error en base de datos al cambiar estado <br> 200: Clase cancelada exitosamente. |
| /clases/(id_ins_clase)/reservar | PUT | id_usuario | 400/401: Error o Instancia de clase no encontrada <br> 402/403: Usuario ya tiene reserva para esta instancia <br> 404/405: Usuario ya tiene reserva para otra clase en ese horario <br> 406: La clase ya se encuentra llena <br> 407/408: Ya existía una reserva (error de BD) <br> 200: Reserva realizada exitosamente. |
| /clases/(id_ins_clase)/verificar | GET | id_usuario | 400/401: Error o Usuario no encontrado <br> 402/403: Error o Instancia de clase no encontrada <br> 404/405: Error o El usuario no se encuentra inscripto <br> 200: El usuario se encuentra inscripto. |
| /clases/(id_clase)/inscripciones | POST | id_usuario | 400/401: Error de validación de listas de espera <br> 200: Se anotó a la lista de espera con éxito. |
| /clases/(id_clase)/confirmar_asistencia | POST | id_usuario | 400/401: Error o Usuario no encontrado <br> 402/403: Error o Clase no encontrada <br> 200: Asistencia registrada con éxito. |
| /clases/(id_clase)/rechazar_asistencia | POST | id_usuario | 400/401: Error o Usuario no encontrado <br> 402/403: Error o Clase no encontrada <br> 200: Asistencia rechazada con éxito. |

Reservas y Cancelaciones

| **Dirección** | **Método** | **Datos necesarios** | **Códigos de respuesta** |
| --- | --- | --- | --- |
| /reservas/(reserva_id)/cancelar | DELETE | - | 400: Error interno al consultar <br> 401: La reserva no existe <br> 402: Error al procesar cancelación en base de datos <br> 200: Cancelación creada exitosamente. |
| /reservas/(id_clase)/confirmar | POST | id_usuario | 404: Usuario, Clase o Lista de espera no encontrada <br> 500: Error de base de datos o lógica al confirmar reserva <br> 200: Confirmación exitosa. |

Mensualidad

| **Dirección** | **Método** | **Datos necesarios** | **Códigos de respuesta** |
| --- | --- | --- | --- |
| /configurar_fin_mensualidad | POST | dni_cliente, id_mensualidad, fecha_fin | 400: El usuario no tiene esa mensualidad <br> 404: No se encontró el usuario <br> 500: Error interno <br> 200: Fin de mensualidad configurado exitosamente. |

Métricas

| **Dirección** | **Método** | **Datos necesarios (Query Params)** | **Códigos de respuesta** |
| --- | --- | --- | --- |
| /metricas/clases_mas_canceladas | GET | limite, id_actividad, fecha_inicio, fecha_fin | 400: No se encontraron clases canceladas <br> 500: Error interno <br> 200: Se devuelve la lista de métricas. |
| /metricas/clases_con_mensualidad | GET | limite, fecha_inicio, fecha_fin | 400: No se encontraron clases <br> 500: Error interno <br> 200: Se devuelve la lista de métricas. |

Notificaciones

| **Dirección** | **Método** | **Datos necesarios** | **Códigos de respuesta** |
| --- | --- | --- | --- |
| /notificaciones/(id_clase) | GET | - | 404: No se encontró la clase <br> 500: Error interno de consulta o fallos del servidor <br> 200: Notificación enviada exitosamente. |

Actividades

| **Dirección** | **Método** | **Datos necesarios** | **Códigos de respuesta** |
| --- | --- | --- | --- |
| /actividades | GET | - | 200: Se devuelve una lista con todas las actividades (vacía si no hay registros). |

Empleados

| **Dirección** | **Método** | **Datos necesarios** | **Códigos de respuesta** |
| --- | --- | --- | --- |
| /empleados | GET | - | 404: No se encontraron empleados <br> 500: Error al obtener empleados <br> 200: Se devuelve una lista de los empleados. |
| /empleados/recepcionistas | POST | dni, nombre, apellido, correo, contraseña, genero | 400: Error al obtener la lista de validación de DNIs <br> 401: El DNI ya se encuentra registrado <br> 402: Error interno al obtener lista de correos <br> 403: El correo ya se encuentra registrado <br> 404: Error en base de datos al insertar el registro <br> 405: El recepcionista no se pudo crear <br> 200: El recepcionista ha sido creado con éxito. |
| /empleados/(empleado_dni) | PUT | dni_nuevo, nombre, apellido, correo, genero, rol_id | 400: Error al obtener la información <br> 401: No existe un empleado con dicho DNI o error listando base <br> 402: El DNI nuevo ya se encuentra registrado para otro empleado <br> 500: Error al intentar modificar <br> 200: Empleado modificado exitosamente. |
| /empleados/(empleado_dni) | DELETE | - | 500: Error al intentar borrar empleado <br> 402: Error al intentar eliminar un empleado con clases <br> 200: Empleado borrado exitosamente. |
| /empleados/(empleado_dni)/desactivar | PATCH | - | 500: Error al intentar borrar/desactivar empleado <br> 200: Empleado desactivado exitosamente. |

Permisos

| **Dirección** | **Método** | **Datos necesarios** | **Códigos de respuesta** |
| --- | --- | --- | --- |
| /empleados/(empleado_dni)/permisos | POST | rol_id | 400: Error de consulta de empleado <br> 401: Empleado no encontrado <br> 402: El empleado ya contaba con ese permiso <br> 500: Error al intentar modificar permiso <br> 200: Permiso modificado correctamente. |

Profesores

| **Dirección** | **Método** | **Datos necesarios** | **Códigos de respuesta** |
| --- | --- | --- | --- |
| /profesores | GET | - | 200: Se devuelve una lista de los profesores registrados. |
| /profesores | POST | dni, nombre, apellido, telefono, genero | 400: Error al intentar listar los DNIs de profesores <br> 401: El DNI ya se encuentra registrado para un profesor <br> 402: Error al intentar insertar el profesor <br> 200: Profesor creado con éxito. |

Salas

| **Dirección** | **Método** | **Datos necesarios** | **Códigos de respuesta** |
| --- | --- | --- | --- |
| /salas | GET | - | 200: Se devuelve una lista de las salas del establecimiento. |

Pagos

| **Dirección** | **Método** | **Datos necesarios** | **Códigos de respuesta** |
| --- | --- | --- | --- |
| /pagos | GET | - | 400: No se encontraron pagos en el sistema <br> 500: Error interno del servidor <br> 200: Se devuelve una lista global con los pagos registrados. |
| /pagos/obtenerQR | GET | - | 200: Devuelve string del QR guardado en el archivo de entorno. |
| /pagos | POST | monto, usuario_id, descripcion, tipo_pago, id_item | 400: Faltan datos requeridos o error al instanciar <br> 500: Error interno de DB o MercadoPago <br> 200: Orden de pago creada exitosamente. |
| /webhook/qr | POST | payload de MercadoPago | -: Procesamiento interno de estado. |
| /pagos/estado/(id_pago) | GET | - | 400: No se encontró el pago <br> 500: Error interno de consulta o validación <br> 200: Datos de la orden obtenidos exitosamente. |

Usuarios

| **Dirección** | **Método** | **Datos necesarios** | **Códigos de respuesta** |
| --- | --- | --- | --- |
| /usuarios | POST | dni, nombre, apellido, contraseña, fecha_nac, correo, telefono, genero, rol_id | 400: Errores lógicos de validación <br> 401: Rol inválido <br> 402: Fecha de nacimiento no válida <br> 403: El usuario debe ser mayor de 14 años <br> 404: Error al obtener listado de DNIs <br> 405: El DNI ya se encuentra registrado <br> 406: Correo ya registrado <br> 500: Error al intentar insertar <br> 200: Usuario registrado exitosamente. |
| /usuarios/(usuario_id)/pagos | GET | - | 400: Error interno de consulta <br> 500: Error del servidor al consultar facturación <br> 200: Se devuelven las transacciones de pago. |
| /usuarios/(usuario_id)/perfil | GET | - | 400: Error interno de consulta <br> 200: Se devuelve la información del perfil del usuario. |
| /usuarios/(usuario_id)/perfil | PUT | dni, nombre, apellido, fecha_nac, correo, telefono | 400: Errores de validación de campos enviados o en DB <br> 402: Error en servidor al comprobar duplicación de correos <br> 403: Validación estricta de edad (< 14 años) <br> 406: El correo electrónico ya se encuentra registrado <br> 500: Error del servidor al procesar modificación <br> 200: Perfil actualizado exitosamente. |
| /usuarios/(usuario_id)/contraseña | PUT | contraseña_actual, contraseña_nueva | 400: La nueva contraseña no cumple validaciones <br> 401: Error interno de consulta de usuario <br> 402: La contraseña actual es incorrecta <br> 403: La nueva contraseña no puede ser igual a la actual <br> 500: Error al modificar el registro <br> 200: Contraseña modificada exitosamente. |
| /usuarios/RestablecerContrasena | POST | correo | 400: El correo electrónico es requerido <br> 401: Error interno de consulta <br> 200: Correo enviado. |
| /usuarios/ConfirmarNuevaContrasena | PUT | nueva_contraseña, correo | 400: Validación de formato incorrecta o campo requerido vacío <br> 401: Error interno de base de datos / usuario no encontrado <br> 402: Nueva contraseña igual a la actual <br> 500: Error interno de base de datos <br> 200: Nueva contraseña confirmada exitosamente. |
| /usuarios/ObtenerListaUsuarios | GET | - | 500: Error de servidor al consultar los registros <br> 200: Se devuelve la lista de usuarios. |
| /usuarios/(usuario_id)/clases | GET | - | 200: "En remodelación." |
| /usuarios/(usuario_id)/avatar | POST | avatar | 400: El parámetro 'avatar' está vacío <br> 401: Error de consulta de usuario <br> 402: Error de servidor al intentar insertar imagen <br> 403: Error de vinculación nula <br> 500: Error de vinculación en DB <br> 200: Avatar subido exitosamente. |
| /usuarios/(usuario_id)/avatar | GET | - | 400: Error interno de consulta de usuario <br> 401: Error de servidor al consultar la imagen <br> 200: Se devuelve el string/data del avatar del usuario. |

## Modelo lógico de la Base de Datos

![Modelo lógico de la Base de Datos](./bd_modelo_logico.png)

## Testing

Para el testing se recomienda hacer archivos de Unit Test con la librería unittest de Python, y que estos archivos se guarden dentro de la carpeta **'/back/test_clases/'**. Esta librería provee una manera y un montón de funciones que permiten hacer el testing de la forma que lo haciamos en Java.
- Para ejecutar estos archivos, hay que correr en la terminal el siguiente comando: *python -m unittest <nombre_del_módulo_a_probar>*

### Testing de Endpoints

Para poder probar los endpoints de la aplicación, se creó la clase _EndpointTestCase_ que se encuentra en **'/back/test_clases'**.
Esta clase a su vez es una subclase de _TestCase_, que es una clase que provee la librería _unittest_ para poder construir
clases de pruebas. La clase _EndpointTestCase_ contiene todo lo esencial para poder realizar pruebas de endpoints, incluyendo:
- Una instancia de la aplicación en modo Testing
- Una conexión a una base de datos de prueba llamada 'test_database.db'
- Un método para decodificar respuestas codificadas en bytes: **decodificarRespByte(resp)**
- Un método para borrar todo lo que se creó para la prueba una vez que estas terminaron.

### Crear un TestCase para un Endpoint en específico

Para crear un TestCase para un Endpoint en específico tienen que crear un archivo en la carpeta **'/back/test_clases/endpoints/'** que lleve el nombre del Endpoint (por ejemplo: _usuarios_services_testcase.py_), y dentro de ese archivo tienen que crear una clase TestCase que herede de _EndpointTestCase_. Si quieren ver como, fijense cómo está implementado en el archivo clases_service_testcase.py.

<br>

La idea es que se cree un método de prueba por cada HU perteneciente a un Endpoint, y que en cada método de prueba se controlen que lo escenarios de esa HU devuelvan el resultado esperado.

### Correr un TestCase

Para correr un TestCase situénse en la carpeta **'/sistema-CEF/back'** y ejecuten el siguiente comando: `python -m unittest test_cases.endpoints.{nombre_testcase}`
