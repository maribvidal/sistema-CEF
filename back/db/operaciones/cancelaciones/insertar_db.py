from db.operaciones.exception_handler import ejecutar_insertar
from db.modulo_fechas import generar_fecha_actual

def insertar_cancelacion(reserva_id, cursor):
    """Operación que permite insertar una cancelación."""
    fecha = generar_fecha_actual()
    query = f"""INSERT INTO Cancelacion (fecha, reserva_id)
                                VALUES ('{fecha}', {reserva_id});"""
    return ejecutar_insertar(query, cursor)
