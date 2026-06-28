from db.operaciones.exception_handler import ejecutar_query 

def borrar_mensualidad(mensualidad_id: int, cursor):
    """Permite borrar una fila de la tabla Mensualidad"""
    query = f"""DELETE FROM Mensualidad WHERE id = {mensualidad_id};"""
    return ejecutar_query(query, cursor)