from db.operaciones.exception_handler import ejecutar_fetchone

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

def verificar_usuario_tenga_mensualidad(usuario_id: int, clase_id: int, cursor) -> dict:
    """Hace una consulta para verificar si un usuario tiene una mensualidad"""
    query = f"""
        SELECT 1
        FROM Clase_tener_Mensualidad ctm
        WHERE ctm.usuario_id = {usuario_id} AND ctm.clase_id = {clase_id}
    """
    return ejecutar_fetchone(query, cursor)
