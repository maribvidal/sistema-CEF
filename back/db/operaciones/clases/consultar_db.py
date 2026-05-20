def listar_clases(cursor) -> list:
    """Hace una consulta para listar todas las clases, y devuelve una lista de tuplas"""
    res = cursor.execute("SELECT * FROM Clase")
    res = res.fetchall()
    return res

def obtener_clase_por_id(cursor, clase_id: int) -> tuple:
    """Hace una consulta para obtener una clase por su ID, y devuelve una tupla con los datos de la clase"""
    res = cursor.execute("SELECT * FROM Clase WHERE id = ?", (clase_id,))
    res = res.fetchone()
    return res
