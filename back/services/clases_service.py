from db.operaciones.conectar_db import conectarse_db
from db.operaciones.commitear_db import commitear
from db.operaciones.clases.consultar_db import listar_clases
from db.operaciones.clases.insertar_db import insertar_clase
from db.operaciones.clases.borrar_db import borrar_clase
from db.operaciones.clases.modificar_db import modificar_clase

def listar_clases_service():
    """Service que lista las clases"""

    cursor = conectarse_db()

    respuesta = listar_clases(cursor)

    if respuesta['status'] == 'error':
        commitear(cursor)
        cursor.connection.close()
        return respuesta

    if respuesta['status'] == 'success' and not respuesta['data']:
        commitear(cursor)
        cursor.connection.close()
        return {
            "error": "No se encontraron clases"
        }, 404

    commitear(cursor)
    cursor.connection.close()
    return {
        "clases": respuesta['data']
    }, 200

def publicar_clase_service(
    estado: str,
    id_actividad: int,
    id_profesor: int
):
    """Service que publica una clase"""

    cursor = conectarse_db()

    respuesta = insertar_clase(estado, id_actividad, id_profesor, cursor)

    if respuesta['status'] == 'error':
        commitear(cursor)
        cursor.connection.close()
        return respuesta

    commitear(cursor)
    cursor.connection.close()
    return {
        "mensaje": "Clase publicada exitosamente."
    }, 201

def modificar_clase_service(
    clase_id: int,
    estado: str,
    id_actividad: int,
    id_profesor: int
):
    """Service que modifica una clase"""

    cursor = conectarse_db()

    respuesta = modificar_clase(cursor, clase_id, estado, id_actividad, id_profesor)

    if respuesta['status'] == 'error':
        commitear(cursor)
        cursor.connection.close()
        return respuesta

    commitear(cursor)
    cursor.connection.close()
    return {
        "mensaje": "Clase modificada exitosamente."
    }, 200

def eliminar_clase_service(clase_id: int):
    """Service que elimina una clase"""

    ## Recibir id del usuario. Buscar rol del usuario.
    ## Si no tiene el permiso necesario, tirar un error.

    cursor = conectarse_db()

    respuesta = borrar_clase(clase_id, cursor)

    if respuesta['status'] == 'error':
        # Hay que avisar si hay pagos pendientes
        cursor.connection.close()
        return respuesta

    commitear(cursor)
    cursor.connection.close()
    return {
        "mensaje": "Clase eliminada exitosamente."
    }, 200
