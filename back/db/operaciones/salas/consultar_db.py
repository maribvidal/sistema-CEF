from db.operaciones.exception_handler import ejecutar_fetchall

def listar_salas(cursor) -> dict:
    """Hace una consulta para listar todas las salas, y devuelve una lista de tuplas"""
    return ejecutar_fetchall("""SELECT s.id, s.nombre
                                FROM Sala s""", cursor)
