from db.operaciones.conectar_db import conectarse_db
from db.operaciones import listar_clases
from db.operaciones_insercion_comunes import publicar_clase

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
    }
