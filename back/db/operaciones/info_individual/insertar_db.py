from db.operaciones.exception_handler import ejecutar_insertar
from utils.modulo_fechas import generar_fecha_actual

def insertar_info_individual(pago_id, inst_clase_id, cursor):
    """Insertar inst_clase_id."""
    query = f"""
        INSERT INTO Info_Individual (pago_id, inst_clase_id, fecha)
                        VALUES  ({pago_id}, {inst_clase_id}, '{generar_fecha_actual()}')
    """
    return ejecutar_insertar(query, cursor)
