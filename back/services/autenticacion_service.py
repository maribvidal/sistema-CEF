from datetime import datetime, timedelta
from db.operaciones.usuarios.consultar_db import consultar_usuario_por_correo
from db.operaciones.conectar_db import conectarse_db
from db.operaciones.commitear_db import commitear
from db.operaciones.usuarios.insertar_db import insertar_usuario
from db.operaciones.usuarios.consultar_db import consultar_usuario_por_dni
from db.operaciones.conectar_db import conectarse_db
from db.operaciones.commitear_db import commitear

import jwt

# Tabla Usuario/Cliente (según consultar_usuario_por_correo)
USR_ID = 0
USR_DNI = 1
USR_NOMBRE = 2
USR_APELLIDO = 3
USR_CORREO = 4
USR_CONTRASENA = 5
USR_FECHA_NAC = 6
USR_TELEFONO = 7
USR_GENERO = 8
USR_ROL = 9

# Tabla Empleado
EMP_ID = 0
EMP_DNI = 1
EMP_NOMBRE = 2
EMP_ROL = 3
EMP_TIPO = 4
EMP_CONTRASENA = 5

# Clave secreta para firmar JWT (en producción, usar variable de entorno)
JWT_SECRET_KEY = "tu-clave-secreta-super-segura-aqui"
JWT_EXPIRATION_HOURS = 24

def login_service(correo: str, contraseña: str) -> tuple:
    """El tipo se refiere a si es cliente, recepcionista 
        o administrador. El rol es necesario para después
        checkear los permisos de ciertos endpoints."""
    cursor = conectarse_db()
    print("Consultando usuario por correo...")
    
    usuario = consultar_usuario_por_correo(correo, cursor)
    commitear(cursor)
    
    print(" resultado consulta usuario: ", dict(usuario['data']) if usuario['data'] else None)
    if usuario["status"] == "error":
        return {
            "error": usuario["message"]
        }, 500
    
    if usuario["status"] == 'success' and usuario["data"] is None:
        return {
            "error": "Usuario no encontrado"
        }, 404

    if usuario['status'] == 'success' and usuario['data'] is not None:
        print("constraseña: ",usuario['data'][USR_CONTRASENA])
        if usuario['data'][USR_CONTRASENA] != contraseña:
            return {"error": "Contraseña incorrecta"}, 400

        # Generar JWT
        token = _generate_jwt({
            "id": usuario['data'][USR_ID],
            "dni": usuario['data'][USR_DNI],
            "nombre": usuario['data'][USR_NOMBRE],
            "tipo": "CLIENTE",
            "rol": ""
        })

        return {
            "mensaje": "Inicio de sesión exitoso",
            "token": token,
            "usuario": {
                "id": usuario['data'][USR_ID],
                "dni": usuario['data'][USR_DNI],
                "nombre": usuario['data'][USR_NOMBRE],
                "tipo": "CLIENTE",
                "rol": ""
            }
        }, 200
    return {"error": "Error desconocido"}, 500
    


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

# Los parametros los tomé en cuenta al ver los text-field del Registro.Vue del frontend, si se necesita agregar o quitar alguno, solo avisenme y lo modifico
def register_service(dni: int, nombre: str, apellido: str, contrasena: str, fecha_nac: str, correo: str, telefono: str, genero: str, rol_id: int):
    # Verificar si el usuario ya existe realizando una constulta a la base de datos
    cursor = conectarse_db()

    print(dni)
    usuario_existente = consultar_usuario_por_dni(dni, cursor)
    print("Consultando usuario por DNI...")
    print("status: ", usuario_existente['status'])
    print("Resultado consulta usuario por DNI: ", dict(usuario_existente['data']) if usuario_existente['data'] else None)
    
    if usuario_existente['status'] == 'success' and usuario_existente['data'] is not None:
        commitear(cursor)
        print("El usuario ya está registrado")
        return False

    # Insertar el nuevo usuario
    resultado = insertar_usuario(dni, nombre, apellido, contrasena, fecha_nac, correo, telefono, genero, rol_id, cursor)
    commitear(cursor)
    if resultado['status'] == 'error':
        print("Error al registrar usuario: ", resultado['message'])
        return {
            "error" : resultado['message']
        }, 500
    print("El usuario registrado exitosamente")
    return {
        "mensaje": "Usuario registrado exitosamente",
        "usuario_id": resultado['data']
    }, 201

def cerrar_sesion():
    # Aca podes implementar la lógica para cerrar sesión.
    return
