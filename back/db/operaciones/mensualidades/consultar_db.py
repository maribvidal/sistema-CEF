from db.operaciones.exception_handler import ejecutar_fetchall, ejecutar_fetchone, ejecutar_query

# REGLAS EXPUESTAS POR EL PROFESOR:
# las mensualidades son de un tipo de actividad, una fecha especifica 1 dia a la semana
# para reservar una clase, el usuario debe tener una mensualidad para esa actividad ??
# un cliente puede tener varias mensualidades para la misma actividad, pero sin pisar las fechas en el mismo horario

# PARA CONSULTAR SI LA MENSUALIDAD CUBRE LA CLASE:
# deberia de obtener las mensualidades del usuario
# verificar que la mensualidad cubra esa clase concreta
# verificar que la fecha de la clase este dentro de la vigencia de la mensualidad
# luego se consulta si se pisa con otra reserva en posterior checkeo
def consultar_mensualidad_cubre_clase(usuario_id: int, clase_id: int, cursor) -> dict:
    pass

def verificar_usuario_tenga_mensualidad_clase(usuario_id: int, clase_id: int, cursor) -> dict:
    """Hace una consulta para verificar si un usuario tiene una mensualidad"""
    query = f"""
        SELECT 1
        FROM Clase_tener_Mensualidad ctm
        INNER JOIN Mensualidad m ON m.id = ctm.mensualidad_id
        WHERE m.usuario_id = {usuario_id} AND ctm.clase_id = {clase_id}
    """
    return ejecutar_fetchone(query, cursor)

def verificar_disponibilidad_usuario(usuario_id: int, clase_id: int, cursor) -> dict:
    """Hace una consulta para verificar si un usuario tiene disponibilidad para inscribirse en una clase"""
    query = f"""
        SELECT 1
        FROM Usuario u
        INNER JOIN Reserva r ON r.usuario_id = u.id
        INNER JOIN Instancia_Clase ic ON ic.id = r.inst_clase_id
        INNER JOIN Clase c ON c.id = ic.clase_id
        WHERE u.id = {usuario_id} AND c.dia = (
            SELECT c2.dia
            FROM Clase c2
            WHERE c2.id = {clase_id}
        ) AND c.hora = (
            SELECT c3.hora
            FROM Clase c3
            WHERE c3.id = {clase_id}
        ) AND ic.fecha = (
            SELECT ic2.fecha
            FROM Instancia_Clase ic2
            WHERE ic2.clase_id = {clase_id}
        )
    """
    return ejecutar_fetchone(query, cursor)

def verificar_usuario_tenga_mensualidad(usuario_id: int, id_mensualidad: int, cursor) -> dict:
    """Hace una consulta para verificar si un usuario tiene una mensualidad"""
    query = f"""
        SELECT 1
        FROM Mensualidad m
        WHERE m.usuario_id = {usuario_id} AND m.id = {id_mensualidad}
    """
    return ejecutar_fetchone(query, cursor)

def obtener_mensualidad_activa(usuario_id: int, id_mensualidad: int, cursor) -> dict:
    """Hace una consulta para obtener la mensualidad activa de un usuario"""
    query = f"""
        SELECT m.fecha_fin
        FROM Mensualidad m
        WHERE m.usuario_id = {usuario_id} AND m.id = {id_mensualidad} AND DATETIME('now') BETWEEN m.fecha_ini AND m.fecha_fin
    """
    return ejecutar_fetchone(query, cursor)

def obtener_mensualidades_activa(cursor) -> dict:
    """Hace una consulta para obtener todas las mensualidades activas"""
    query = f"""
        SELECT m.id, m.fecha_fin
        FROM Mensualidad m
        WHERE DATETIME('now') BETWEEN m.fecha_ini AND m.fecha_fin
    """
    return ejecutar_fetchall(query, cursor)

def obtener_mensualidad_activa_por_usuario(usuario_id: int, cursor) -> dict:
    """Hace una consulta para obtener la mensualidad activa de un usuario"""
    query = f"""
        SELECT m.id, m.fecha_fin
        FROM Mensualidad m
        WHERE m.usuario_id = {usuario_id} AND DATETIME('now') BETWEEN m.fecha_ini AND m.fecha_fin
    """
    return ejecutar_fetchall(query, cursor)

def obtener_mensualidad_por_id(id_mensualidad: int, cursor) -> dict:
    """Hace una consulta para obtener la mensualidad por su ID"""
    query = f"""
        SELECT *
        FROM Mensualidad m
        WHERE m.id = {id_mensualidad}
    """
    return ejecutar_fetchone(query, cursor)

def obtener_clase_mensualidad(id_mensualidad: int, cursor) -> dict:
    """Hace una consulta para obtener la clase de una mensualidad"""
    query = f"""
        SELECT ctm.clase_id
        FROM Clase_tener_Mensualidad ctm
        WHERE ctm.mensualidad_id = {id_mensualidad}
    """
    return ejecutar_fetchone(query, cursor)


def obtener_todas_las_mensualidades_usuario(usuario_id: int, cursor) -> dict:
    """Hace una consulta para obtener todas las mensualidades de un usuario"""
    query = f"""
        SELECT *
        FROM Mensualidad
        WHERE usuario_id = {usuario_id}
    """
    return ejecutar_fetchall(query, cursor)