from db.operaciones.conectar_db import conectarse_db

def consultar_usuario_por_dni(dni: int) -> tuple:
    """Hace una consulta por un Usuario con un dni pasado por parámetro,
        y devuelve una tupla"""
    cursor = conectarse_db()
    res = cursor.execute("SELECT * FROM Usuario WHERE dni = ?", (dni,))
    res = res.fetchone()
    cursor.connection.close()
    return res

def consultar_usuario_por_correo(correo: str) -> tuple:
    """Hace una consulta por un Usuario con un correo pasado por parámetro,
        y devuelve una tupla"""
    cursor = conectarse_db()
    res = cursor.execute("SELECT * FROM Usuario WHERE correo = ?", (correo,))
    res = res.fetchone()
    cursor.connection.close()
    return res

def consultar_usuario_por_id(id: int) -> tuple:
    """Hace una consulta por un Usuario con un id pasado por parámetro,
        y devuelve una tupla"""
    cursor = conectarse_db()
    res = cursor.execute("SELECT * FROM Usuario WHERE id = ?", (id,))
    res = res.fetchone()
    cursor.connection.close()
    return res

def listar_usuarios() -> list:
    """Hace una consulta para listar todos los usuarios, y devuelve una lista de tuplas"""
    cursor = conectarse_db()
    res = cursor.execute("SELECT * FROM Usuario")
    res = res.fetchall()
    cursor.connection.close()
    return res
