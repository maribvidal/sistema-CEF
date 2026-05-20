from db.operaciones.conectar_db import conectarse_db

def listar_clases() -> list:
    """Hace una consulta para listar todas las clases, y devuelve una lista de tuplas"""
    cursor = conectarse_db()
    res = cursor.execute("SELECT * FROM Clase")
    res = res.fetchall()
    cursor.connection.close()
    return res

def obtener_clase_por_id(clase_id: int) -> tuple:
    """Hace una consulta para obtener una clase por su ID, y devuelve una tupla con los datos de la clase"""
    cursor = conectarse_db()
    res = cursor.execute("SELECT * FROM Clase WHERE id = ?", (clase_id,))
    res = res.fetchone()
    cursor.connection.close()
    return res
