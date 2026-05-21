from db.operaciones.exception_handler import ejecutar_fetchall, ejecutar_fetchone

def consultar_usuario_por_dni(dni: int, cursor) -> dict:
    """Hace una consulta por un Usuario con un dni pasado por parámetro,
        y devuelve una tupla"""
    query = f"SELECT * FROM Usuario WHERE dni = {dni}"
    return ejecutar_fetchone(query, cursor)

def consultar_usuario_por_correo(correo: str, cursor) -> dict:
    """Hace una consulta por un Usuario con un correo pasado por parámetro,
        y devuelve una tupla"""
    query = f"""
            SELECT *
            FROM Usuario
            WHERE correo = '{correo}'
        """
    return ejecutar_fetchone(query, cursor)

def consultar_usuario_por_id(id: int, cursor) -> dict:
    """Hace una consulta por un Usuario con un id pasado por parámetro,
        y devuelve una tupla"""
    query = f"""
        SELECT * 
        FROM Usuario
        WHERE id = {id}"""
    return ejecutar_fetchone(query, cursor)

def listar_usuarios(cursor) -> dict:
    """Hace una consulta para listar todos los usuarios, y devuelve una lista de tuplas"""
    return ejecutar_fetchall("SELECT * FROM Usuario LEFT JOIN Cuenta ON Usuario.dni = Cuenta.dni", cursor)
