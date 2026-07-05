from db.operaciones.exception_handler import ejecutar_fetchone, ejecutar_fetchall

def verificar_asistencia_usuario_clase(id_usuario: int, id_clase: int, cursor):
    """Operación que consulta por asistencias según el id del usuario y el id de la clase
        asociada a la asistencia."""
    query = f"""SELECT 1
                FROM Asistencias_Clase a 
                WHERE a.usuario_id = {id_usuario} AND a.inst_clase_id = {id_clase};"""
    return ejecutar_fetchone(query, cursor);

def obtener_clases_con_mensualidad_mas_concurridas(fecha_inicio, fecha_fin, cursor):
    """Operación que obtiene las clases con mensualidad más concurridas."""
    query = f"""
        SELECT c.id AS clase_id, COUNT(DISTINCT a.usuario_id) AS cantidad_asistencias
        FROM Asistencias_Clase a
        INNER JOIN Instancia_Clase ic ON a.inst_clase_id = ic.id
        INNER JOIN Clase c ON ic.clase_id = c.id
        WHERE a.con_mensualidad = 1
    """

    if fecha_inicio is not None and fecha_fin is not None:
        query += f" AND ic.fecha BETWEEN '{fecha_inicio}' AND '{fecha_fin}'"
    
    query += """
        GROUP BY c.id
        ORDER BY cantidad_asistencias DESC;
    """
    
    return ejecutar_fetchall(query, cursor);