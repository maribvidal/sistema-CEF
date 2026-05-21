from db.operaciones.exception_handler import ejecutar_fetchall, ejecutar_fetchone

def obtener_rol_por_id(id: int, cursor) -> dict:
    """Hace una consulta por un Rol con un id pasado por parámetro,
        y devuelve un diccionario"""
    query = f"SELECT * FROM Rol WHERE id = {id}"
    res = ejecutar_fetchone(query, cursor)
    return res
