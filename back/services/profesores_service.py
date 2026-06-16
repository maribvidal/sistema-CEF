from db.operaciones.conectar_db import conectarse_db
from db.operaciones.profesores.consultar_db import listar_profesores, listar_dnis_profesores
from db.operaciones.profesores.insertar_db import insertar_profesor

def listar_profesores_service():
    """Service que lista los profesores."""
    cursor = conectarse_db()
    respuesta = listar_profesores(cursor)
    cursor.connection.close()
    return respuesta, 200

def crear_profesor_service(dni, nombre, apellido, telefono, genero):
    """Service que crea un profesor."""

    cursor = conectarse_db()

    # Comprobar que el DNI no se encuentre registrado

    res_dnis = listar_dnis_profesores(cursor)

    if res_dnis['status'] == 'error':
        cursor.connection.close()
        return {
            "error": "Hubo un error tratando de listar los DNIs de los profesores.",
            "message": res_dnis['message']
        }, 400

        for res_dni in res_dnis['data']:
            if (str(dni) == res_dni['dni']):
                cursor.connection.close()
                return {
                    "error": "El DNI ya se encuentra registrado para un profesor."
                }, 401

    # Intentar insertar el nuevo profesor

    res_insertar = insertar_profesor(nombre, apellido, telefono, genero, dni, cursor)

    if res_insertar['status'] == 'error':
        cursor.connection.close()
        return {
            "error": res_insertar['message']
        }, 402

    cursor.connection.commit()
    cursor.connection.close()

    return {
        "message": f"El profesor con id {res_insertar['data']} ha sido creado con éxito."
    }, 200
