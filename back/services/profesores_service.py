from db.operaciones.conectar_db import conectarse_db
from db.operaciones.profesores.consultar_db import listar_profesores, listar_dnis_profesores
from db.operaciones.profesores.insertar_db import insertar_profesor

def listar_profesores_service():
    """Service que lista los profesores."""
    cursor = conectarse_db()
    respuesta = listar_profesores(cursor)
    cursor.connection.close()
    return respuesta, 200

def crear_profesor_service(dni, nombre, apellido, telefono, genero, actividades: list):
    """Service que crea un profesor y le asigna sus actividades."""

    if not actividades: # Si la lista es None o está vacía []
        return {
            "error": "Un profesor debe tener al menos una actividad asignada."
        }, 400 # Bad Request

    cursor = conectarse_db()

    # comprobamos que el DNI no se encuentre registrado
    res_dnis = listar_dnis_profesores(cursor)

    if res_dnis['status'] == 'error':
        cursor.connection.close()
        return {
            "error": "Hubo un error tratando de listar los DNIs de los profesores.",
            "details": res_dnis['message']
        }, 500 # Internal Server Error 

    # Bucle corregido (Tenia problema de identación)
    for res_dni in res_dnis['data']:
        if str(dni) == str(res_dni['dni']):
            cursor.connection.close()
            return {
                "error": "El DNI ya se encuentra registrado para un profesor."
            }, 409 # Conflict (El recurso ya existe y por lo tanto causa conflicto)

    # Intentamos insertar el nuevo profesor (Ahora agregando también las actividades)
    res_insertar = insertar_profesor(nombre, apellido, telefono, genero, dni, actividades, cursor)

    if res_insertar['status'] == 'error':
        cursor.connection.close()
        return {
            "error": "Error al insertar el profesor en la base de datos.",
            "details": res_insertar['message']
        }, 500 # Internal Server Error

    cursor.connection.commit()
    cursor.connection.close()

    return {
        "message": f"El profesor con id {res_insertar['data']} ha sido creado con éxito."
    }, 200 # Se ha creado con éxito