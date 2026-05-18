from db.operaciones.consultar_db import listar_clases

def listar_clases_service():
    """Service que lista las clases"""
    clases = listar_clases()
    
    if not clases:
        return {
            "error": "No se encontraron clases"
        }, 404
        
    # verificar si es que no tengo que hacer un for para agregar cada clase
    return {
        "clases": clases
    }, 200
