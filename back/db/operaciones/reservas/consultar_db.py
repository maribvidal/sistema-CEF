from db.operaciones.exception_handler import ejecutar_fetchone, ejecutar_fetchall
from enums.dias import Dias

def consultar_reserva_por_id(reserva_id: int, cursor):
    """Operación que consulta por una reserva según su id y devuelve una tupla."""
    query = f"SELECT * FROM Reserva WHERE id = {reserva_id}"
    return ejecutar_fetchone(query, cursor)

def obtener_reservas_usuario_dia_hora(id_usuario: int, dia: Dias, hora: str, cursor):
    """Operación que consulta por reservas según el id del usuario, y el dia y hora
        de la instancia de la clase asociada con la reserva."""
    query = f"""SELECT r.usuario_id, r.inst_clase_id, r.fecha
                FROM Reserva r INNER JOIN Instancia_Clase ic ON (r.inst_clase_id = ic.id)
                                INNER JOIN Clase c ON (ic.clase_id = c.id)
                                INNER JOIN Usuario u ON (r.usuario_id = u.id)
                WHERE r.usuario_id = {id_usuario} AND c.dia = '{dia}' AND c.hora = '{hora}';"""
    return ejecutar_fetchall(query, cursor)
 
def obtener_reservas_usuario_inst_clase(id_ins_clase: int, id_usuario: int, cursor):
    """Operación que consulta por reservas según el id de la instancia de la clase, y del
        id del usuario asociados a la reserva."""
    query = f"SELECT * FROM Reserva WHERE usuario_id = {id_usuario} AND inst_clase_id = {id_ins_clase};"
    return ejecutar_fetchall(query, cursor)

def consultar_reserva_por_usuario_clase(id_usuario: int, id_clase: int, cursor):
    """Operación que consulta por reservas según el id del usuario y el id de la clase asociada a la reserva."""
    query = f"""SELECT 1
                FROM Reserva r 
                WHERE r.usuario_id = {id_usuario} AND r.inst_clase_id = {id_clase};"""
    return ejecutar_fetchone(query, cursor)