def consultar_usuario_por_dni(cursor, dni: int) -> tuple:
    """Hace una consulta por un Usuario con un dni pasado por parámetro,
        y devuelve una tupla"""
    query = f"SELECT * FROM Usuario WHERE dni = {dni}"
    res = cursor.execute(query)
    return res.fetchone()

def consultar_usuario_por_correo(cursor, correo: str) -> tuple:
    """Hace una consulta por un Usuario con un correo pasado por parámetro,
        y devuelve una tupla"""
    query = f"""
            SELECT 
                u.id,
                c.dni,
                u.fecha_nac,
                u.telefono,
                c.nombre,
                c.apellido,
                c.correo,
                c.contraseña,
                c.genero
            FROM Usuario u
            INNER JOIN Cuenta c ON u.dni = c.dni  
            WHERE c.correo = '{correo}'
        """
    res = cursor.execute(query)
    return res.fetchone()

def consultar_usuario_por_id(cursor, id: int) -> tuple:
    """Hace una consulta por un Usuario con un id pasado por parámetro,
        y devuelve una tupla"""
    query = f"""
        SELECT 
            c.id, c.dni, c.nombre, c.apellido, c.contraseña, u.fecha_nac, c.correo, u.telefono, c.genero 
        FROM Usuario u
        INNER JOIN Cuenta c ON u.dni = c.dni
        WHERE c.id = {id}"""
    res = cursor.execute(query)
    return res.fetchone()

def listar_usuarios(cursor) -> list:
    """Hace una consulta para listar todos los usuarios, y devuelve una lista de tuplas"""
    query = "SELECT * FROM Usuario LEFT JOIN Cuenta ON Usuario.dni = Cuenta.dni"
    res = cursor.execute(query)
    return res.fetchall()
