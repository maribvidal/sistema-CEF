from db.operaciones.exception_handler import ejecutar_fetchall, ejecutar_fetchone

def consultar_sala_por_id(id: int, cursor) -> dict:
    """Hace una consulta para devolver la tupla de una sala por su id."""
    return ejecutar_fetchone(f"SELECT * FROM Sala WHERE id = {id};", cursor)

def listar_salas(cursor) -> dict:
    """Hace una consulta para listar todas las salas, y devuelve una lista de tuplas"""
    return ejecutar_fetchall("""SELECT s.id, s.nombre
                                FROM Sala s""", cursor)

def consultar_sala_por_dia_hora(dia: str, hora: str, cursor) -> dict:
    """Hace una consulta para devolver la tupla de una sala por el día y hora
        en el que transcurra una clase.."""
    return ejecutar_fetchone(f"""SELECT s.id, s.nombre
                                FROM Sala s
                                JOIN Clase c ON s.id = c.sala_id
                                WHERE c.dia = '{dia}' AND c.hora = '{hora}';""", cursor)
