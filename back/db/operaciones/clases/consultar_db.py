from db.operaciones.exception_handler import ejecutar_fetchall, ejecutar_fetchone

def listar_clases(cursor) -> dict:
    """Hace una consulta para listar todas las clases, y devuelve una lista de tuplas"""
    return ejecutar_fetchall("""SELECT c.estado, c.actividad_id, c.profesor_id, cos.fecha, cos.hora, cos.sala_id
                                FROM Clase c INNER JOIN Clase_Ocurrir_Sala cos ON c.id = cos.clase_id""", cursor)

def consultar_clase_por_id(clase_id, cursor) -> dict:
    """Hace una consulta para obtener una clase por su ID, y devuelve una tupla con los datos de la clase"""
    return ejecutar_fetchone(f"SELECT * FROM Clase WHERE id = {clase_id}", cursor)
