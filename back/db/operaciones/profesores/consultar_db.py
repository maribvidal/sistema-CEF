from db.operaciones.exception_handler import ejecutar_fetchall

def listar_profesores(cursor) -> dict:
    """Hace una consulta para listar todos los profesores, y devuelve una lista de tuplas"""
    return ejecutar_fetchall("SELECT * FROM Usuario WHERE rol_id = 5", cursor)

def listar_dnis_profesores(cursor) -> dict:
    """Hace una consulta para listar todos los dnis de los
        profesores, y devuelve una lista de tuplas."""
    return ejecutar_fetchall("SELECT dni FROM Usuario WHERE rol_id = 5", cursor)
