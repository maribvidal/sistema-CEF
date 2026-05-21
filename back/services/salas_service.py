from db.operaciones.conectar_db import conectarse_db
from db.operaciones.salas.consultar_db import listar_salas

def listar_salas_service():
    """Service que lista las salas"""
    cursor = conectarse_db()
    respuesta = listar_salas(cursor)
    cursor.connection.close()
    return respuesta, 200
