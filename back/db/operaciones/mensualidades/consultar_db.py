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
    """Devuelve 1 si el usuario tiene al menos una mensualidad que cubre la clase."""
    queryRelacionandoConActividad = f"""
        SELECT *
        FROM Mensualidad m
        INNER JOIN Clase_Tener_Mensualidad ctm ON ctm.mensualidad_id = m.id
        INNER JOIN Clase c ON c.id = ctm.clase_id
        INNER JOIN Actividad a ON a.id = c.actividad_id
        WHERE 
            m.usuario_id = {usuario_id} -- obtiene las mensualidades del usuario 
            AND a.nombre = (
                SELECT a2.nombre
                FROM Clase c2
                INNER JOIN Actividad a2 ON a2.id = c2.actividad_id
                WHERE c2.id = {clase_id}
            ) -- verifica el obtener las mensualidades de la misma actividad de la clase
            AND (
                SELECT c3.fecha
                FROM Clase_Ocurrir_Sala c3
                WHERE c3.clase_id = {clase_id}
            ) BETWEEN m.fecha_ini AND m.fecha_fin -- verifica si hay alguna mensualidad que tenga vigencia dentro del periodo de la clase
    """
    
    querySinRelacionarConActividad = f"""
        SELECT 1
        FROM Mensualidad m
        WHERE 
            m.usuario_id = {usuario_id} -- obtiene las mensualidades del usuario 
            AND (
                SELECT c3.fecha
                FROM Clase_Ocurrir_Sala c3
                WHERE c3.clase_id = {clase_id}
            ) BETWEEN m.fecha_ini AND m.fecha_fin -- verifica si hay alguna mensualidad que tenga vigencia dentro del periodo de la clase
    """
    
    return ejecutar_fetchone(querySinRelacionarConActividad, cursor)