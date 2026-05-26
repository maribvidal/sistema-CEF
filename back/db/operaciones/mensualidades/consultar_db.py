from db.operaciones.exception_handler import ejecutar_fetchall, ejecutar_fetchone

# REGLAS EXPUESTAS POR EL PROFESOR:
# las mensualidades son de un tipo de actividad, una fecha especifica 1 dia a la semana
# para reservar una clase, el usuario debe tener una mensualidad para esa actividad ??
# un cliente puede tener varias mensualidades para la misma actividad, pero sin pisar las fechas en el mismo horario

def consultar_mensualidad_cubre_clase(usuario_id: int, clase_id: int, cursor) -> dict:
    """Hace una consulta para verificar si la mensualidad de un usuario cubre una clase, y devuelve 1 si es así"""
    "No tiene en consideracion que el usuario tiene varias mensualidades"
    "No verifica si la mensualidad tiene el mismo tipo de actividad que la clase"
    "No verifica que la mensualidad tenga alguna semana libre para reservar y que coincida con la semana de la clase"
    query = f"""
        SELECT 1
        FROM Clase_Ocurrir_Sala c
        WHERE 
            c.id = {clase_id} 
            and c.fecha BETWEEN (
                SELECT fecha_ini 
                FROM Mensualidad 
                WHERE usuario_id = {usuario_id} 
            ) AND (
                SELECT fecha_fin 
                FROM Mensualidad 
                WHERE usuario_id = {usuario_id}  
            )
    """
    return ejecutar_fetchone(query, cursor)