from db.operaciones.exception_handler import ejecutar_query

def borrar_imagen_por_id(id: int, cursor):
    """Permite borrar una fila de la tabla Imagen por su id"""
    query = f"DELETE FROM Imagen WHERE id = {id};"
    return ejecutar_query(query, cursor)
