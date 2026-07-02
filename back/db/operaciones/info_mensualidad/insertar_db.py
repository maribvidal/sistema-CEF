from db.operaciones.exception_handler import ejecutar_insertar
from utils.modulo_fechas import generar_fecha_actual

def insertar_info_mensualidad(id_mensualidad, clase_id, cursor):
    """Insertar info_mensualidad."""
    query = f"""
        INSERT INTO Info_Mensualidad (mensualidad_id, clase_id, fecha)
                        VALUES  ({id_mensualidad}, {clase_id}, '{generar_fecha_actual()}')
    """
    return ejecutar_insertar(query, cursor)
