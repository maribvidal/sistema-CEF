from db.operaciones.exception_handler import ejecutar_fetchall, ejecutar_fetchone

def listar_actividades(cursor) -> dict:
    """Hace una consulta para listar todas las actividades, y devuelve una lista de tuplas"""
    return ejecutar_fetchall("SELECT * FROM Actividad", cursor)