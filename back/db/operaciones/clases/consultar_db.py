from db.operaciones.exception_handler import ejecutar_fetchall, ejecutar_fetchone

def listar_clases(cursor) -> dict:
    """Hace una consulta para listar todas las clases, y devuelve una lista de tuplas"""
    return ejecutar_fetchall("""SELECT *
                                FROM Clase""", cursor)

def listar_clases_ocurriendo(cursor) -> dict:
    """Hace una consulta para listar todas las clases, junto con la información obtenida
        de la tabla Clase_Ocurrir_Sala, y devuelve una lista de tuplas."""
    return ejecutar_fetchall("""SELECT c.id, c.estado, c.actividad_id, c.profesor_id, cos.dia, cos.hora, cos.sala_id, c.cupo_maximo
                                FROM Clase c INNER JOIN Clase_Ocurrir_Sala cos ON c.id = cos.clase_id""", cursor)

def consultar_clase_por_id(clase_id, cursor) -> dict:
    """Hace una consulta para obtener una clase por su ID, y devuelve una tupla con los datos de la clase"""
    return ejecutar_fetchone(f"SELECT * FROM Clase WHERE id = {clase_id}", cursor)

def consultar_disponibilidad_clase(clase_id, cursor) -> dict:
    """Hace una consulta para obtener la disponibilidad de una clase por su ID, y devuelve 1 si hay disponibilidad"""
    query = f"""
        SELECT 1
        FROM Clase c
        WHERE c.id = {clase_id} and c.cupo_maximo > (
            SELECT COUNT(*) 
            FROM Usuario_Inscribir_Clase 
            WHERE clase_id = {clase_id}
        )
    """
    return ejecutar_fetchone(query, cursor)