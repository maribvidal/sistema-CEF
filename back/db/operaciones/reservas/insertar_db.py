from db.operaciones.exception_handler import ejecutar_insertar
from db.modulo_fechas import generar_fecha_actual

def insertar_reserva(usuario_id: int, inst_clase_id: int, cursor):
    """ Permite insertar una reserva de parte de un usuario a
        una instancia de una clase. """
    fecha = generar_fecha_actual()
    query = f"""
        INSERT INTO Reserva (usuario_id, inst_clase_id, fecha)
        VALUES              ({usuario_id}, {inst_clase_id}, '{fecha}');
    """
    return ejecutar_insertar(query, cursor)
