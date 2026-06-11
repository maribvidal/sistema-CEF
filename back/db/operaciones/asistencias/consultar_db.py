from db.operaciones.exception_handler import ejecutar_fetchone, ejecutar_fetchall

def verificar_asistencia_usuario_clase(id_usuario: int, id_clase: int, cursor):
    """Operación que consulta por asistencias según el id del usuario y el id de la clase
        asociada a la asistencia."""
    query = f"""SELECT 1
                FROM Asistencia a 
                WHERE a.usuario_id = {id_usuario} AND a.inst_clase_id = {id_clase};"""
    return ejecutar_fetchone(query, cursor);