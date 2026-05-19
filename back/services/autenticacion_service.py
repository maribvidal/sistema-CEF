from db.operaciones.empleados.consultar_db import buscar_empleado_por_correo
from db.operaciones.usuarios.consultar_db import consultar_usuario_por_correo

# Tabla Usuario/Cliente
USR_ID = 0
USR_NOMBRE = 2
USR_CONTRASENA = 5

# Tabla Empleado
EMP_ID = 0
EMP_NOMBRE = 2
EMP_TIPO = 3
EMP_ROL = 4
EMP_CONTRASENA = 5

def login_service(correo: str, contraseña: str):
    """El tipo se refiere a si es cliente, recepcionista 
        o administrador. El rol es necesario para después
        checkear los permisos de ciertos endpoints."""
    usuario = consultar_usuario_por_correo(correo)

    if usuario['status'] == 'success' and usuario['data'] is not None:
        if usuario['data'][USR_CONTRASENA] != contraseña:
            return {"error": "Contraseña incorrecta"}, 400

        return {
            "mensaje": "Inicio de sesión exitoso",
            "usuario": {
                "id": usuario['data'][USR_ID],
                "nombre": usuario['data'][USR_NOMBRE],
                "tipo": "CLIENTE",
                "rol": ""
            }
        }, 200

    empleado = buscar_empleado_por_correo(correo)
    
    if empleado['status'] == 'error':
        return empleado

    if empleado['status'] == 'success' and empleado['data'] is None:
        return {"error": "Usuario no registrado"}, 404

    if empleado['status'] == 'success' and empleado['data'][EMP_CONTRASENA] != contraseña:
        return {"error": "Contraseña incorrecta"}, 400

    return {
        "mensaje": "Inicio de sesión exitoso",
        "usuario": {
            "id": empleado['data'][EMP_ID],
            "nombre": empleado['data'][EMP_NOMBRE],
            "tipo": empleado['data'][EMP_TIPO],
            "rol": empleado['data'][EMP_ROL]
        }
    }, 200


from db.operaciones.usuarios.insertar_db import insertar_usuario
from db.operaciones.usuarios.consultar_db import consultar_usuario_por_dni
# Los parametros los tomé en cuenta al ver los text-field del Registro.Vue del frontend, si se necesita agregar o quitar alguno, solo avisenme y lo modifico
def register_service(dni: int, nombre: str, apellido: str, contrasena: str, fecha_nac: str, correo: str, telefono: str) -> bool:
    # Verificar si el usuario ya existe realizando una constulta a la base de datos
    if consultar_usuario_por_dni(dni):
        print("El usuario ya está registrado")
        return False

    # Insertar el nuevo usuario
    insertar_usuario(dni, nombre, apellido, contrasena, fecha_nac, correo, telefono, "Otro")
    print("El usuario registrado exitosamente")
    return True

def cerrar_sesion():
    # Aca podes implementar la lógica para cerrar sesión.
    return