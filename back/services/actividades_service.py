from db.operaciones.conectar_db import conectarse_db
from db.operaciones.actividades.consultar_db import listar_actividades

def listar_actividades_service():
    """Service que lista las actividades"""
    cursor = conectarse_db()
    respuesta = listar_actividades(cursor)
    cursor.connection.commit()
    cursor.connection.close()
    # No devolvemos 404 si está vacío para que el select del front no falle, solo devolvemos la lista vacía
    return respuesta, 200
