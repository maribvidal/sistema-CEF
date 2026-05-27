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

def consultar_cliente_por_id(id: int, cursor) -> dict:
    """Hace una consulta por un Usuario con un id pasado por parámetro,
        y devuelve una tupla"""
    query = f"""
        SELECT * 
        FROM Usuario
        WHERE id = {id}"""
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
    return ejecutar_fetchall("SELECT * FROM Usuario", cursor)

def obtener_clases_usuario(id_usuario: int, cursor) -> dict:
    """Hace una consulta para obtener las clases a las que un usuario está inscrito,
        y devuelve una lista de tuplas"""
    query = f"""
        SELECT 
            cos.fecha,
            cos.hora,
            c.estado,
            a.nombre AS nombre_actividad,
            p.nombre AS nombre_profesor,
            s.nombre AS nombre_sala
        FROM Clase c
        INNER JOIN Usuario_Inscribir_Clase i ON (c.id = i.clase_id)
        INNER JOIN Actividad a ON (c.actividad_id = a.id)
        INNER JOIN Profesor p ON (c.profesor_id = p.id)
        INNER JOIN Clase_Ocurrir_Sala cos ON (c.id = cos.clase_id)
        INNER JOIN Sala s ON (cos.sala_id = s.id)
        WHERE i.usuario_id = {id_usuario}
    """
    return ejecutar_fetchall(query, cursor)