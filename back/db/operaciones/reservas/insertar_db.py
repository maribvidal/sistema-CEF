from db.operaciones.exception_handler import ejecutar_insertar
from utils.modulo_fechas import generar_fecha_actual

def insertar_reserva(usuario_id: int, inst_clase_id: int, cursor):
    """ Permite insertar una reserva de parte de un usuario a
        una instancia de una clase. """
    fecha = generar_fecha_actual()
    query = f"""
        INSERT INTO Reserva (usuario_id, inst_clase_id, fecha)
        VALUES              ({usuario_id}, {inst_clase_id}, '{fecha}');
    """
    return ejecutar_insertar(query, cursor)

# Esta funcion habria que verificar que se haga todo o nada y que ademas antes de eliminar verificar si esta en una lista u otra
def confirmar_reserva(usuario_id: int, inst_clase_id: int, cursor):
    """ Permite confirmar una reserva de parte de un usuario a una instancia de una clase. """
    fecha = generar_fecha_actual()
    query = f"""
        DELETE FROM Lista_Espera_Abonados
        WHERE usuario_id = {usuario_id} AND inst_clase_id = {inst_clase_id};
        
        DELETE FROM Lista_Espera_Individual
        WHERE usuario_id = {usuario_id} AND inst_clase_id = {inst_clase_id};
        
        INSERT INTO Reserva (usuario_id, inst_clase_id, fecha)
        VALUES ({usuario_id}, {inst_clase_id}, '{fecha}');
    """
    return ejecutar_insertar(query, cursor)