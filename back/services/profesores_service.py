from db.operaciones.conectar_db import conectarse_db
from db.operaciones.profesores.consultar_db import listar_profesores
from db.operaciones.profesores.insertar_db import insertar_profesor

def listar_profesores_service():
    """Service que lista los profesores."""
    cursor = conectarse_db()
    respuesta = listar_profesores(cursor)
    cursor.connection.close()
    return respuesta, 200

def crear_profesor_service(dni, nombre, apellido, genero):
    """Service que crea un profesor."""

    cursor = conectarse_db()

    # Intentar insertar el nuevo profesor

    res_insertar = insertar_profesor(nombre, apellido, genero, dni, cursor)

    if res_insertar['status'] == 'error':
        cursor.connection.close()
        return {
            "error": res_insertar['message']
        }, 400

    cursor.connection.commit()
    cursor.connection.close()

    return {
        "mensaje": f"El profesor con id {res_insertar['data']} ha sido creado con éxito."
    }, 200
