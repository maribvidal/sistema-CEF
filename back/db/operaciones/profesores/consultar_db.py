from db.operaciones.exception_handler import ejecutar_fetchall, ejecutar_fetchone

def listar_profesores(cursor) -> dict:
    """Hace una consulta para listar todos los profesores, y devuelve una lista de tuplas"""
    return ejecutar_fetchall("SELECT * FROM Usuario WHERE rol_id = 5", cursor)