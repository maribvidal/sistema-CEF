from db.operaciones.exception_handler import ejecutar_fetchall, ejecutar_fetchone

def listar_clases(cursor) -> list:
    """Hace una consulta para listar todas las clases, y devuelve una lista de tuplas"""
    return ejecutar_fetchall("SELECT * FROM Clase", cursor)

def consultar_clase_por_id(clase_id, cursor) -> tuple:
    """Hace una consulta para obtener una clase por su ID, y devuelve una tupla con los datos de la clase"""
    return ejecutar_fetchone(f"SELECT * FROM Clase WHERE id = {clase_id}", cursor)
