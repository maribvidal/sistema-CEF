from db.operaciones.exception_handler import ejecutar_fetchall, ejecutar_fetchone
from db import Dias

def listar_clases(cursor) -> dict:
    """Hace una consulta para listar todas las clases, y devuelve una lista de tuplas"""
    return ejecutar_fetchall("""SELECT *
                                FROM Clase""", cursor)

def consultar_clase_por_id(clase_id, cursor) -> dict:
    """Hace una consulta para obtener una clase por su ID, y devuelve una tupla con los datos de la clase"""
    return ejecutar_fetchone(f"SELECT * FROM Clase WHERE id = {clase_id}", cursor)

def consultar_clase_por_sala_dia_hora(id_sala: int, dia: str, hora: str, cursor) -> dict:
    """Hace una consulta para devolver la tupla de una clase por
        el id_sala, el dia y la hora."""
    return ejecutar_fetchone(f"SELECT * FROM Clase WHERE sala_id = {id_sala} AND dia = '{dia}' AND hora = '{hora}';", cursor)

def obtener_detalles_clase(id_clase: int, cursor) -> dict:
    """Hace una consulta para obtener los detalles de una clase por su ID, y devuelve una tupla con los datos de la clase"""
    query = f"""
        SELECT a.nombre AS nombre_actividad, c.dia, c.hora, ic.fecha
        FROM Clase c
        INNER JOIN Actividad a ON c.actividad_id = a.id
        INNER JOIN Instancia_Clase ic ON c.id = ic.clase_id
        WHERE c.id = {id_clase}
    """
    return ejecutar_fetchone(query, cursor)