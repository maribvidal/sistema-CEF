from db.operaciones.exception_handler import ejecutar_fetchall, ejecutar_fetchone

def consultar_usuario_por_dni(dni: int) -> tuple:
    """Hace una consulta por un Usuario con un dni pasado por parámetro,
        y devuelve una tupla"""
    query = f"SELECT * FROM Usuario WHERE dni = {dni}"
    return ejecutar_fetchone(query)

def consultar_usuario_por_correo(correo: str) -> tuple:
    """Hace una consulta por un Usuario con un correo pasado por parámetro,
        y devuelve una tupla"""
    query = f"""
            SELECT * 
            FROM Usuario
            INNER JOIN Cuenta c ON Usuario.dni = c.dni  
            WHERE c.correo = '{correo}'
        """
    return ejecutar_fetchone(query)

def consultar_usuario_por_id(id: int) -> tuple:
    """Hace una consulta por un Usuario con un id pasado por parámetro,
        y devuelve una tupla"""
    query = f"SELECT * FROM Usuario WHERE id = {id}"
    return ejecutar_fetchone(query)

def listar_usuarios() -> list:
    """Hace una consulta para listar todos los usuarios, y devuelve una lista de tuplas"""
    return ejecutar_fetchall("SELECT * FROM Usuario")
