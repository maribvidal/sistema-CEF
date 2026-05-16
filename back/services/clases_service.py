from db.operaciones import insertar_clase, eliminar_clase, cancelar_clase, modificar_clase, listar_clases

def listar_clases_service():
    clases = listar_clases()
    
    if not clases:
        return {
            "error": "No se encontraron clases"
        }, 404
        
    # verificar si es que no tengo que hacer un for para agregar cada clase
    return {
        "clases": clases
    }, 200