from db.operaciones.exception_handler import ejecutar_query

def cambiar_estado_info_mensualidad(id_mensualidad: int, cursor):
    """Permite cambiar el estado de un Info_Mensualidad."""
    query = f"UPDATE Info_Mensualidad SET renovar = 1 WHERE mensualidad_id = {id_mensualidad}"
    ejecutar_query(query, cursor)
