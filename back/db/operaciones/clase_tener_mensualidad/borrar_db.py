from db.operaciones.exception_handler import ejecutar_query 

def borrar_clase_tener_mensualidad(mensualidad_id: int, cursor):
    """Permite borrar una fila de la tabla Clase_Tener_Mensualidad"""
    query = f"""DELETE FROM Clase_Tener_Mensualidad WHERE mensualidad_id = {mensualidad_id};"""
    return ejecutar_query(query, cursor)