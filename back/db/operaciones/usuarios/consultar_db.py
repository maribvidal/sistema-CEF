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

def obtener_clase_usuario_fecha_hora(id_usuario: int, fecha, hora, cursor) -> dict:
    """Hace una consulta para obtener la clase a la que está inscripto
        un usuario en una fecha y hora determinada, si es que el 
        usuario está inscripto a una clase en esa fecha y hora."""
    # Utilizo ejecutar_fetchall por si el usuario llega a estar metido
    # en más de una clase en la misma fecha y hora (lo cual sería un error)
    query = f"""
            SELECT
                cos.id
            FROM Usuario u
                INNER JOIN Usuario_Inscribir_Clase uic ON (u.id = uic.usuario_id)
                INNER JOIN Clase_Ocurrir_Sala cos ON (uic.clase_ocurrir_sala_id = cos.id)
            WHERE u.id = {id_usuario} AND cos.fecha = '{fecha}' AND cos.hora = '{hora}'
            """
    return ejecutar_fetchall(query, cursor)

def listar_dnis_usuarios(cursor) -> dict:
    """Hace una consulta para retornar todos los dnis registrados
        de los usuarios."""
    query = "SELECT dni FROM Usuario WHERE rol_id = 3"
    return ejecutar_fetchall(query, cursor)
