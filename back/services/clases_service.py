from db.operaciones.conectar_db import conectarse_db
from db.operaciones import listar_clases
from db.operaciones_insercion_comunes import publicar_clase
from db.operaciones_eliminar_comunes import eliminar_clase_por_id
from db.operaciones_modificar_comunes import modificar_clase

def listar_clases_service():
    """Service que lista las clases"""

    cursor = conectarse_db()

    clases = listar_clases(cursor)
    
    if not clases:
        cursor.connection.close()
        return {
            "error": "No se encontraron clases"
        }, 404
        
    cursor.connection.close()
    return {
        "clases": clases
    }, 200

def publicar_clase_service(
    estado: str,
    id_actividad: int,
    id_profesor: int
):
    """Service que publica una clase"""

    cursor = conectarse_db()

    respuesta = publicar_clase(cursor, estado, id_actividad, id_profesor)

    if respuesta == -1:
        cursor.connection.close()
        return {
            "error": "Error al publicar la clase."
        }, 400
    
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

    if (not respuesta):
        cursor.connection.close()
        return {
            "error": "Error al modificar la clase."
        }, 400

    cursor.connection.close()
    return {
        "mensaje": "Clase modificada exitosamente."
    }, 200

def eliminar_clase_service(clase_id: int):
    """Service que elimina una clase"""

    cursor = conectarse_db()

    respuesta = eliminar_clase_por_id(cursor, clase_id)

    if (not respuesta):
        cursor.connection.close()
        return {
            "error": "Error al eliminar la clase."
        }, 400

    cursor.connection.close()
    return {
        "mensaje": "Clase eliminada exitosamente."
    }, 200
