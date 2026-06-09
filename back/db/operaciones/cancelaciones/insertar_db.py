from db.operaciones.exception_handler import ejecutar_insertar
from db.modulo_fechas import generar_fecha_actual

def insertar_cancelacion(usuario_id, inst_clase_id, cursor):
    """Operación que permite insertar una cancelación."""
    fecha = generar_fecha_actual()
    query = f"""INSERT INTO Cancelacion (fecha, usuario_id, inst_clase_id)
                                VALUES ('{fecha}', {usuario_id}, {inst_clase_id});"""
    return ejecutar_insertar(query, cursor)
