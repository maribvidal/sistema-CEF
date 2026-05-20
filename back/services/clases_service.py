from db.operaciones import listar_clases
from db.operaciones.conectar_db import conectarse_db
from db.operaciones.commitear_db import commitear

def listar_clases_service():
    """Service que lista las clases"""
    cursor = conectarse_db()
    clases = listar_clases(cursor)
    commitear(cursor)
    if not clases:
        return {
            "error": "No se encontraron clases"
        }, 404
        
    return {
        "clases": clases
    }, 200
