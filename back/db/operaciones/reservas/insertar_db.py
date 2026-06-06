from db.operaciones.exception_handler import ejecutar_insertar

def insertar_reserva(usuario_id: int, inst_clase_id: int, cursor):
    """ Permite insertar una reserva de parte de un usuario a
        una instancia de una clase. """
    fecha = "2026-02-02" # Valor dummy por ahora. Mañana voy a implementar un módulo que se encarga de las fechas
    query = f"""
        INSERT INTO Reserva (usuario_id, inst_clase_id, fecha)
        VALUES              ({usuario_id}, {inst_clase_id}, '{fecha}');
    """
    return ejecutar_insertar(query, cursor)
