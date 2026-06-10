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
    return ejecutar_fetchall("SELECT * FROM Usuario WHERE rol_id IN (0, 1, 2, 3, 4)", cursor)

def obtener_clases_usuario(id_usuario: int, cursor) -> dict:
    """Hace una consulta para obtener las clases a las que un usuario está inscrito,
        y devuelve una lista de tuplas"""
    query = f"""
        SELECT c.id, c.estado, c.actividad_id, c.profesor_id, c.sala_id, c.dia, c.hora, c.cupo_maximo, c.monto
        FROM Clase c INNER JOIN Instancia_Clase ic ON (c.id = ic.clase_id)
                    INNER JOIN Reserva r ON (ic.id = r.inst_clase_id)
                    INNER JOIN Usuario u ON (r.usuario_id = u.id)
        WHERE u.id = {id_usuario}"""
    return ejecutar_fetchall(query, cursor)

def obtener_clase_usuario_fecha(id_usuario: int, fecha: str, cursor) -> dict:
    """Hace una consulta para obtener la clase a la que está inscripto
        un usuario en una fecha y hora determinada, si es que el 
        usuario está inscripto a una clase en ese día y hora."""
    # Utilizo ejecutar_fetchall por si el usuario llega a estar metido
    # en más de una clase en la misma fecha y hora (lo cual sería un error)
    # Lozi: Claro, ya que esa ese escenario nunca ocurriria porque lo pararia el inscribir_clase_service
    query = f"""
        SELECT c.id,
        c.estado,
        c.actividad_id,
        c.profesor_id,
        c.sala_id,
        c.dia,
        c.hora,
        c.cupo_maximo,
        c.monto
        FROM Reserva r
        JOIN Instancia_Clase ic ON r.inst_clase_id = ic.id
        JOIN Clase c ON ic.clase_id = c.id
        WHERE r.usuario_id = {id_usuario}
        AND ic.fecha = '{fecha}'
    """
    return ejecutar_fetchall(query, cursor)

def listar_dnis_usuarios(cursor) -> dict:
    """Hace una consulta para retornar todos los dnis registrados
        de los usuarios."""
    query = "SELECT dni FROM Usuario WHERE rol_id = 3"
    return ejecutar_fetchall(query, cursor)

def verificar_usuario_abonado(cursor, id_usuario: int) -> bool:
    """Hace una consulta para verificar si un usuario es abonado o no."""
    query = f"""
        SELECT *
        FROM Usuario
        INNER JOIN Mensualidad m ON Usuario.id = m.usuario_id
        WHERE Usuario.id = {id_usuario};"""
    resultado = ejecutar_fetchone(query, cursor)
    return resultado is not None