from db.operaciones.conectar_db import conectarse_db

def consultar_permiso_por_id(id: int) -> tuple:
    """Hace una consulta por un Permiso con un id pasado por parámetro,
        y devuelve una tupla"""
    cursor = conectarse_db()
    res = cursor.execute(f"SELECT id FROM Permiso WHERE id = {id}")
    res = res.fetchone()
    cursor.connection.close()
    try:
        return res[0]
    except TypeError:
        print("No se encontró el permiso con el id proporcionado.")
        return()
