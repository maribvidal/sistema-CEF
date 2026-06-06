from db.operaciones.exception_handler import ejecutar_fetchall

def consultar_sala_por_id(id: int, cursor) -> dict:
    """Hace una consulta para devolver la tupla de una actividad por su id."""
    return ejecutar_fetchone(f"SELECT * FROM Sala WHERE id = {id};", cursor)

def listar_salas(cursor) -> dict:
    """Hace una consulta para listar todas las salas, y devuelve una lista de tuplas"""
    return ejecutar_fetchall("""SELECT s.id, s.nombre
                                FROM Sala s""", cursor)
