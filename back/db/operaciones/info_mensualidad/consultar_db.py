from db.operaciones.exception_handler import ejecutar_fetchall, ejecutar_fetchone, ejecutar_query

def comprobar_existe_info_mensualidad(id_mensualidad: int, cursor) -> dict:
    """Hace una consulta para verificar si existe un Info_Mensualidad."""
    query = f"""
        SELECT id
        FROM Info_Mensualidad
        WHERE mensualidad_id = {id_mensualidad}
    """
    return ejecutar_fetchone(query, cursor)
