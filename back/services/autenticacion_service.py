from datetime import datetime, timedelta
from pprint import pprint
from db.operaciones.clases.consultar_db import consultar_clase_por_id
from db.operaciones.reservas.consultar_db import obtener_reserva_usuario_inst_clase
from db.operaciones.usuarios.consultar_db import consultar_usuario_por_correo
from db.operaciones.conectar_db import conectarse_db
from db.operaciones.usuarios.insertar_db import insertar_usuario
from db.operaciones.usuarios.consultar_db import consultar_usuario_por_dni
from db.operaciones.conectar_db import conectarse_db
from db.operaciones.instancias_clases.consultar_db import consultar_instancia_clase_por_id
from db.operaciones.usuarios.consultar_db import obtener_estado_usuario

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
    print(" resultado consulta usuario: ", dict(usuario['data']) if usuario['data'] else None)
    if usuario["status"] == "error":
        cursor.connection.close()
        return {
            "error": usuario["message"]
        }, 500


    # ------------- VERIFICACIÓN DE ESTADO DEL USUARIO (CORREO VERIFICADO) -------------
    usuario_id = usuario['data']['id']
    estado_usuario = obtener_estado_usuario(usuario_id, cursor)
    if estado_usuario['status'] == 'error':
        print("Error al obtener el estado del usuario: ", estado_usuario['message'])
        cursor.connection.close()
        return {
            "error": estado_usuario['message']
        }, 500
    elif estado_usuario['data']['estado'] == 0:
        cursor.connection.close()
        print("El usuario existe pero el correo no está verificado")
        return {
            "error": "El correo del usuario no está verificado."
        }, 401
    print("El usuario existe y su correo está verificado")
    # ------------- FIN VERIFICACIÓN ESTADO DE USUARIO (CORREO VERIFICADO) -------------

    if usuario['status'] == 'success' and usuario['data'] is not None:
        if usuario['data']['contraseña'] != contraseña:
            cursor.connection.close()
            return {"error": "Contraseña incorrecta"}, 400

        # Generar JWT
        token = _generate_jwt({
            "id": usuario['data']['id'],
            "dni": usuario['data']['dni'],
            "nombre": usuario['data']['nombre'],
            "tipo": "CLIENTE" if usuario['data']['rol_id'] == 3 else "STAFF",
            "rol": usuario['data']['rol_id']
        })

        cursor.connection.commit()
        cursor.connection.close()
        return {
            "message": "Inicio de sesión exitoso",
            "token": token,
            "usuario": {
                "id": usuario['data']['id'],
                "dni": usuario['data']['dni'],
                "nombre": usuario['data']['nombre'],
                "tipo": "CLIENTE" if usuario['data']['rol_id'] == 3 else "STAFF",
                "rol": usuario['data']['rol_id']
            }
        }, 200
    
    cursor.connection.close()
    # Si por alguna razón no se cumplió ninguna de las condiciones, pues me hago el boludo y devuelvo datos incorrectos, ya que no se contempla en la HU otro escenario
    # Cambio 500 por error 400, solo en caso de que pase algo falopa
    return {"error": "Datos Incorrectos"}, 400
    


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
        cursor.connection.close()
        print("El usuario ya está registrado")
        return False

    # Insertar el nuevo usuario
    resultado = insertar_usuario(dni, nombre, apellido, contrasena, fecha_nac, correo, telefono, genero, rol_id, cursor)
    if resultado['status'] == 'error':
        cursor.connection.close()
        print("Error al registrar usuario: ", resultado['message'])
        return {
            "error" : resultado['message']
        }, 500
    print("El usuario registrado exitosamente")
    cursor.connection.commit()
    cursor.connection.close()
    return {
        "message": "Usuario registrado exitosamente",
        "usuario_id": resultado['data']
    }, 200

def cerrar_sesion():
    # Aca podes implementar la lógica para cerrar sesión.
    return

def validar_reserva_service(inst_clase_id: int, id_usuario: int):

    # Primero verificamos que en la tabla Reserva exista una reserva con id_cliente e id_inst_clase.
    cursor = conectarse_db()
    reserva = obtener_reserva_usuario_inst_clase(
        id_usuario=id_usuario, 
        id_ins_clase=inst_clase_id, 
        cursor=cursor
    )

    if reserva['status'] == 'error':
        cursor.connection.close()
        return {
            "error": reserva['message']
        }, 500
    # fetchall puede devolver una lista vacía cuando no existen reservas
    if not reserva['data']:
        cursor.connection.close()
        return {
            "error": "No se encontró una reserva para ese cliente en esa clase."
        }, 404

    instancia_res = consultar_instancia_clase_por_id(inst_clase_id, cursor)

    if instancia_res is None or instancia_res['status'] == 'error':
        cursor.connection.close()
        return {"error": "No se encontró la instancia de la clase."}, 404

    id_clase = instancia_res['data']['clase_id']
    fecha_instancia = instancia_res['data']['fecha'] # Ej: "2026-06-22"

    clase_res = consultar_clase_por_id(id_clase, cursor)
    if clase_res is None or clase_res['status'] == 'error':
        cursor.connection.close()
        return {"error": "No se encontró la clase asociada."}, 404

    hora_clase = clase_res['data']['hora'] # Ej: 12:30 o 12:30:00

    fecha_hora_str = f"{fecha_instancia} {hora_clase}"
    print(fecha_hora_str)

    # Mejor hago esto por si las dudas para parsear mejor
    try:
        # Asumiendo que la BD trae segundos
        fecha_hora_clase_dt = datetime.strptime(fecha_hora_str, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        # Si falla, es porque la BD no trae segundos (12:30)
        fecha_hora_clase_dt = datetime.strptime(fecha_hora_str, "%Y-%m-%d %H:%M")

    # Calculo límites absolutos
    limite_inferior = fecha_hora_clase_dt - timedelta(minutes=30)
    limite_superior = fecha_hora_clase_dt + timedelta(minutes=30)
    hora_actual = datetime.now()

    print("Hora actual: ", hora_actual)
    print("Límite inferior: ", limite_inferior)
    print("Límite superior: ", limite_superior)

    # Clausular de Guarda de tiempo
    if hora_actual < limite_inferior:
        cursor.connection.close()
        return {"error": "La clase aún no ha comenzado. Puedes validar tu asistencia 30 minutos antes de la clase."}, 422

    if hora_actual > limite_superior:
        cursor.connection.close()
        return {"error": "La reserva expiró. La clase comenzó hace más de 30 minutos."}, 409

    cursor.connection.close()
    return {"message": "Asistencia confirmada exitosamente"}, 200


def validar_reserva_dni_service(inst_clase_id: int, dni: int):
    cursor = conectarse_db()
    usuario = consultar_usuario_por_dni(dni, cursor)

    if usuario['status'] == 'error':
        cursor.connection.close()
        return {
            "error": "Error al consultar usuario por DNI.",
            "details": usuario['message']
        }, 500
    if usuario['data'] is None:
        cursor.connection.close()
        return {
            "error": "No se encontró un usuario con ese DNI."
        }, 404

    cursor.connection.close()

    id_usuario = usuario['data']['id']
    return validar_reserva_service(inst_clase_id, id_usuario)

