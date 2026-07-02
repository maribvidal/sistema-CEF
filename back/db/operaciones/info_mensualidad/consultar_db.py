from db.operaciones.exception_handler import ejecutar_fetchall, ejecutar_fetchone, ejecutar_query

def comprobar_existe_info_mensualidad(id_mensualidad: int, cursor) -> dict:
    """Hace una consulta para verificar si existe un Info_Mensualidad."""
    query = f"""
        SELECT id
        FROM Info_Mensualidad
        WHERE mensualidad_id = {id_mensualidad}
    """
    return ejecutar_fetchone(query, cursor)

def consultar_info_mensualidad(id_inf: int, cursor) -> dict:
    query = f"""
        SELECT *
        FROM Info_Mensualidad
        WHERE id = {id_inf}
    """
    return ejecutar_fetchone(query, cursor)
