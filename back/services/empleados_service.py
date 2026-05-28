from db.operaciones.conectar_db import conectarse_db
from db.operaciones.empleados.consultar_db import listar_empleados
from db.operaciones.empleados.insertar_db import insertar_recepcionista
from db.operaciones.empleados.modificar_db import modificar_empleado, borrar_empleado, desactivar_empleado, modificar_empleado_con_dni
from db.operaciones.empleados.consultar_db import listar_empleados_desactivados, listar_correos_empleados, listar_dnis_empleados

def listar_empleados_service():
    """Service que lista los empleados."""
    cursor = conectarse_db()
    respuesta = listar_empleados(cursor)
    cursor.connection.close()

    if respuesta['status'] == 'error':
        return {
            "error": "Error al obtener empleados.",
            "message": respuesta['message']
        }, 500
    elif respuesta['status'] == 'success' and not respuesta['data']:
        return {
            "error": "No se encontraron empleados."
        }, 404

    return respuesta['data'], 200

def modificar_empleado_service(
    empleado_dni: int,
    dni_nuevo: int, 
    nombre: str, 
    apellido: str, 
    correo: str, 
    contraseña: str, 
    fecha_nac: str, 
    telefono: str, 
    genero: str, 
    rol_id: int
    ):
    """Service que modifica un empleado."""
    cursor = conectarse_db()

    # Comprobar que el dni al que se quiere cambiar no esté siendo
    # utilizado por otro empleado

    res_dnis = listar_dnis_empleados(cursor)

    if res_dnis['status'] == 'error':
        cursor.connection.close()
        return {
            "error": "Error al obtener los DNIs de los empleados."
        }, 400

    if (str(dni_nuevo) in str(res_dnis['data'])):
        cursor.connection.close()
        return {
            "error": "El DNI ya se encuentra registrado para un empleado."
        }, 401

    respuesta = modificar_empleado_con_dni(empleado_dni, dni_nuevo, nombre, apellido, correo, contraseña, fecha_nac, telefono, genero, rol_id, cursor)

    # Con esto guardo los cambios en la base de datos
    cursor.connection.commit()
    cursor.connection.close()

    if respuesta['status'] == 'error':
        return {
            "error": "Error al intentar modificar empleado.",
            "message": respuesta['message']
        }, 500
    return respuesta, 200

def borrar_empleado_service(empleado_dni: int):
    """Service que borra un empleado."""
    cursor = conectarse_db()
    respuesta = borrar_empleado(empleado_dni, cursor)

    if respuesta['status'] == 'error':
        return {
            "error": "Error al intentar borrar empleado.",
            "message": respuesta['message']
        }, 500

    cursor.connection.commit()
    cursor.connection.close()

    return respuesta['data'], 200

def desactivar_empleado_service(empleado_dni: int):
   """Service que desactiva un empleado.""" 

   cursor = conectarse_db()
   respuesta = desactivar_empleado(empleado_dni, cursor)
   cursor.connection.close()

   if respuesta['status'] == 'error':
       return {
           "error": "Error al intentar borrar empleado.",
           "message": respuesta['message']
       }, 500
# ESTO NO ES NECESARIO: CUANDO HAGO EJECUTAR QUERY ME DEVUELVE "SUCCESS" PRO CON DATA = NONE, y eso no significa que no se encontró el empleado, sino que se ejecutó la consulta pero no devuelve datos, lo cual es normal porque es un UPDATE, no un SELECT
#    elif respuesta['status'] == 'success' and not respuesta['data']: 
#        return {
#            "error": "No se encontraron empleados"
#        }, 404
   return respuesta['data'], 200

def listar_empleados_desactivados_service():
    """Service que lista los empleados desactivados."""
    cursor = conectarse_db()
    respuesta = listar_empleados_desactivados(cursor)
    cursor.connection.close()

    if respuesta['status'] == 'error':
        return {
            "error": "Error al obtener empleados desactivados.",
            "message": respuesta['message']
        }, 500
    elif respuesta['status'] == 'success' and not respuesta['data']:
        return {
            "error": "No se encontraron empleados desactivados."
        }, 404

    return respuesta['data'], 200

def crear_recepcionista_service(dni, nombre, apellido, correo, contraseña, genero):
    """Service que crea un recepcionista."""

    # ¿Comprobar los valores enviados?

    cursor = conectarse_db()

    # Comprobar que el DNI no se haya utilizado

    res_dnis = listar_dnis_empleados(cursor)

    if res_dnis['status'] == 'error':
        cursor.connection.close()
        return {
            "error": "Error al obtener los DNIs de los empleados."
        }, 400

    if (dni in str(res_dnis['data'])):
        cursor.connection.close()
        return {
            "error": "El DNI ya se encuentra registrado para un empleado."
        }, 401

    # Comprobar que el correo tampoco se haya utilizado

    res_correos = listar_correos_empleados(cursor)

    if res_correos['status'] == 'error':
        cursor.connection.close()
        return {
            "error": "Error al obtener los correos de los empleados."
        }, 402

    if (correo in str(res_correos['data'])):
        cursor.connection.close()
        return {
            "error": "El correo ya se encuentra registrado para un empleado."
        }, 403

    # Intentar insertar al recepcionista

    res_insertar = insertar_recepcionista(dni, nombre, apellido, correo, contraseña, genero, cursor)

    if res_insertar['status'] == 'error':
        cursor.connection.close()
        return {
            "error": res_insertar['message']
        }, 404

    if res_insertar['status'] == 'success' and (not res_insertar['data']):
        cursor.connection.close()
        return {
            "error": "El recepcionista no se pudo crear por alguna razón desconocida."
        }, 405

    cursor.connection.commit()
    cursor.connection.close()

    return {
        "mensaje": "El recepcionista ha sido creado con éxito."
    }, 200
