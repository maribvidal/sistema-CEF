from db.operaciones.exception_handler import ejecutar_fetchall, ejecutar_fetchone

def consultar_actividad_por_id(id: int, cursor) -> dict:
    """Hace una consulta para devolver la tupla de una actividad por su id."""
    return ejecutar_fetchone(f"SELECT * FROM Actividad WHERE id = {id};", cursor)

def listar_actividades(cursor) -> dict:
    """Hace una consulta para listar todas las actividades, y devuelve una lista de tuplas"""
    return ejecutar_fetchall("SELECT * FROM Actividad", cursor)
