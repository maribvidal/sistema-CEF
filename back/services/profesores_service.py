from db.operaciones.conectar_db import conectarse_db
from db.operaciones.commitear_db import commitear
from db.operaciones.profesores.consultar_db import listar_profesores

def listar_profesores_service():
    """Service que lista los profesores"""
    cursor = conectarse_db()
    respuesta = listar_profesores(cursor)
    commitear(cursor)
    cursor.connection.close()
    return respuesta, 200
