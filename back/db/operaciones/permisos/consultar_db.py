from db.operaciones.exception_handler import ejecutar_fetchall, ejecutar_fetchone

def consultar_permiso_por_id(id: int, cursor) -> dict:
    """Hace una consulta por un Permiso con un id pasado por parámetro,
        y devuelve una tupla"""
    query = f"SELECT id FROM Permiso WHERE id = {id}" 
    res = ejecutar_fetchone(query, cursor)
    return res
