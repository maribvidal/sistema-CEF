from db.operaciones.conectar_db import conectarse_db

def obtener_rol_por_id(id: int) -> tuple:
    """Hace una consulta por un Rol con un id pasado por parámetro,
        y devuelve una tupla"""
    cursor = conectarse_db()
    res = cursor.execute("SELECT * FROM Rol WHERE id = ?", (id,))
    res = res.fetchone()
    cursor.connection.close()
    return res
