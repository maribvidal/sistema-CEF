import jwt
from datetime import datetime, timedelta
from db.operaciones.consultar_db import buscar_empleado_por_correo, consultar_usuario_por_correo
from db.operaciones.empleados.consultar_db import buscar_empleado_por_correo
from db.operaciones.usuarios.consultar_db import consultar_usuario_por_correo
from db.operaciones.conectar_db import conectarse_db
from db.operaciones.commitear_db import commitear

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

# Clave secreta para firmar JWT (en producción, usar variable de entorno)
JWT_SECRET_KEY = "tu-clave-secreta-super-segura-aqui"
JWT_EXPIRATION_HOURS = 24

def login_service(correo: str, contraseña: str):
    """El tipo se refiere a si es cliente, recepcionista 
        o administrador. El rol es necesario para después
        checkear los permisos de ciertos endpoints."""
    cursor = conectarse_db()
    usuario = consultar_usuario_por_correo(correo, cursor)

    if usuario['status'] == 'success' and usuario['data'] is not None:
        commitear(cursor)
        if usuario['data'][USR_CONTRASENA] != contraseña:
            return {"error": "Contraseña incorrecta"}, 400

        # Generar JWT
        token = _generate_jwt({
            "id": usuario["id"],
            "nombre": usuario["nombre"],
            "tipo": "CLIENTE",
            "rol": ""
        })

        return {
            "mensaje": "Inicio de sesión exitoso",
            "token": token,
            "usuario": {
                "id": usuario['data'][USR_ID],
                "nombre": usuario['data'][USR_NOMBRE],
                "tipo": "CLIENTE",
                "rol": ""
            }
        }, 200

    empleado = buscar_empleado_por_correo(correo, cursor)
    
    commitear(cursor)
    if empleado['status'] == 'error':
        return empleado

    if empleado['status'] == 'success' and empleado['data'] is None:
        return {"error": "Usuario no registrado"}, 404

    if empleado['status'] == 'success' and empleado['data'][EMP_CONTRASENA] != contraseña:
        return {"error": "Contraseña incorrecta"}, 400

    # Generar JWT
    token = _generate_jwt({
        "id": empleado["id"],
        "nombre": empleado["nombre"],
        "tipo": empleado["tipo"],
        "rol": empleado["rol"]
    })

    return {
        "mensaje": "Inicio de sesión exitoso",
        "token": token,
        "usuario": {
            "id": empleado['data'][EMP_ID],
            "nombre": empleado['data'][EMP_NOMBRE],
            "tipo": empleado['data'][EMP_TIPO],
            "rol": empleado['data'][EMP_ROL]
        }
    }, 200

def _generate_jwt(user_data):
    """Genera un JWT token con los datos del usuario."""
    payload = {
        **user_data,
        "iat": datetime.utcnow(),
        "exp": datetime.utcnow() + timedelta(hours=JWT_EXPIRATION_HOURS)
    }
    token = jwt.encode(payload, JWT_SECRET_KEY, algorithm="HS256")
    return token

def verify_jwt(token):
    """Verifica y decodifica un JWT token."""
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

from db.operaciones.usuarios.insertar_db import insertar_usuario
from db.operaciones.usuarios.consultar_db import consultar_usuario_por_dni
from db.operaciones.conectar_db import conectarse_db
from db.operaciones.commitear_db import commitear
# Los parametros los tomé en cuenta al ver los text-field del Registro.Vue del frontend, si se necesita agregar o quitar alguno, solo avisenme y lo modifico
def register_service(dni: int, nombre: str, apellido: str, contrasena: str, fecha_nac: str, correo: str, telefono: str) -> bool:
    # Verificar si el usuario ya existe realizando una constulta a la base de datos
    cursor = conectarse_db()

    usuario_existente = consultar_usuario_por_dni(dni, cursor)

    if usuario_existente['status'] == 'success' and usuario_existente['data'] is not None:
        commitear(cursor)
        print("El usuario ya está registrado")
        return False

    # Insertar el nuevo usuario
    insertar_usuario(dni, nombre, apellido, contrasena, fecha_nac, correo, telefono, "Otro", cursor)
    commitear(cursor)
    print("El usuario registrado exitosamente")
    return True

def cerrar_sesion():
    # Aca podes implementar la lógica para cerrar sesión.
    return
