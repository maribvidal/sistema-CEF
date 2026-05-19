from db.operaciones.conectar_db import conectarse_db

def listar_clases() -> list:
    """Hace una consulta para listar todas las clases, y devuelve una lista de tuplas"""
    cursor = conectarse_db()
    res = cursor.execute("SELECT * FROM Clase")
    res = res.fetchall()
    cursor.connection.close()
    return res