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

def consultar_cupo_disponible_por_clase(id_clase: int, cursor) -> dict:
    """Hace una consulta que devuelve la cantidad de cupo disponible para una clase."""
    query = f"""
        SELECT cupo_maximo
        FROM Clase
        WHERE id = {id_clase}
    """
    return ejecutar_fetchone(query, cursor)

def obtener_cantidad_reservar_instancia_clase(id_instancia: int, cursor) -> dict:
    """Hace una consulta que devuelve la cantidad de reservas existentes para una instancia de clase."""
    query = f"""
        SELECT COUNT(*) AS cantidad_reservas
        FROM Reserva
        WHERE inst_clase_id = {id_instancia}
    """
    return ejecutar_fetchone(query, cursor)

def consultar_reservas_instancias_por_clase(id_clase: int, cursor) -> dict:
    """Hace una consulta que devuelve la cantidad de reservas por instancia de clase.
       Devuelve una fila por cada instancia_clase de la clase indicada con su conteo de reservas."""
    query = f"""
        SELECT c.id,
               ic.id AS inst_clase_id,
               COUNT(r.id) AS cantidad_reservas
        FROM Clase c
            INNER JOIN Instancia_Clase ic ON c.id = ic.clase_id
            LEFT JOIN Reserva r ON ic.id = r.inst_clase_id
        WHERE c.id = {id_clase}
        GROUP BY c.id, ic.id
    """

    return ejecutar_fetchall(query, cursor)

def consultar_reservas_total_por_clase(id_clase: int, cursor) -> dict:
    """Hace una consulta que devuelve la cantidad total de reservas de todas las instancias de una clase."""
    query = f"""
        SELECT r.id
        FROM Clase c
            INNER JOIN Instancia_Clase ic ON c.id = ic.clase_id
            LEFT JOIN Reserva r ON ic.id = r.inst_clase_id
        WHERE c.id = {id_clase};
    """

    return ejecutar_fetchone(query, cursor)

def consultar_instancias_por_clase_id(id_clase: int, cursor) -> dict:
    """Hace una consulta que devuelve los ids de todas las instancias
        de clases que posea una clase, y hace la consulta con el
        id de la clase recibido."""
    query = f"""
        SELECT ic.id, ic.fecha
        FROM Clase c
            INNER JOIN Instancia_Clase ic ON c.id = ic.clase_id
        WHERE c.id = {id_clase}
    """

    return ejecutar_fetchall(query, cursor)

def consultar_clase_por_id_instancia(instancia_id: int, cursor) -> dict:
    """Hace una consulta que devuelve la clase a la que pertenece
        una instancia de clase, y hace la consulta con el id de
        la instancia recibido."""
    query = f"""
        SELECT c.id, c.actividad_id, c.sala_id, c.profesor_id, c.dia, c.hora, c.cupo_maximo, c.monto, c.estado
        FROM Clase c
            INNER JOIN Instancia_Clase ic ON c.id = ic.clase_id
        WHERE ic.id = {instancia_id}
    """

    return ejecutar_fetchone(query, cursor)

def comprobar_vigencia_clases(tuplas: list, cursor) -> list:
    """Recibe una lista de tuplas de clases y devuelve una lista filtrada
        con las clases que tengan instancias vigentes (fecha >= hoy)"""
    clases_vigentes = []
    for tup in tuplas:
        id_instancia = tup["inst_clase_id"]
        query = f"""
            SELECT fecha
            FROM Instancia_Clase
            WHERE id = {id_instancia} AND fecha >= DATE('now');
        """
        resultado = ejecutar_fetchone(query, cursor)
        if resultado['data'] is not None:
            clases_vigentes.append(tup)
    return clases_vigentes