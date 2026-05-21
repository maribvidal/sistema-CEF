from db.operaciones.exception_handler import ejecutar_query 

def borrar_clase(cursor, clase_id):
    """Elimina una clase de la base de datos por su ID."""
    query = f"DELETE FROM Clase WHERE id = {clase_id}"
    return ejecutar_query(query, cursor)
