from db.operaciones.exception_handler import ejecutar_fetchone, ejecutar_fetchall

def consultar_cancelacion_por_id(cancelacion_id: int, cursor):
    """Operación que consulta por una cancelacion según su id y devuelve una tupla."""
    query = f"SELECT * FROM Cancelacion WHERE id = {cancelacion_id}"
    return ejecutar_fetchone(query, cursor)

def obtener_cancelaciones_por_usuario_inst_clase(id_ins_clase: int, id_usuario: int, cursor):
    """Operación que consulta por una cancelación según el id de la instancia de la clase
        de la reserva vinculada con la cancelación, y del usuario de la reserva."""
    query = f"""SELECT *
                FROM Cancelacion
                WHERE usuario_id = {id_usuario} AND inst_clase_id = {id_ins_clase};"""
    return ejecutar_fetchall(query, cursor)

def obtener_clases_mas_canceladas(cursor, actividad=None, fecha_inicio=None, fecha_fin=None):
    """Operación que consulta por todas las clases más canceladas."""
    query = f"""
                SELECT cl.dia, cl.hora, a.nombre as actividad, COUNT(*) as cancelaciones
                FROM Cancelacion c
                INNER JOIN Instancia_Clase ic ON c.inst_clase_id = ic.id
                INNER JOIN Clase cl ON ic.clase_id = cl.id
                INNER JOIN Actividad a ON cl.actividad_id = a.id
            """

    condiciones = []
    if actividad:
        condiciones.append(f"a.id = {actividad}")
    
    # esto lo filtraria por fecha de cancelacion o por la fecha de la instancia de la clase?
    if fecha_inicio and fecha_fin:
        # por cancelacion: 
        # condiciones.append(f"c.fecha >= '{fecha_inicio}' AND c.fecha <= '{fecha_fin}'")
        
        # por instancia de clase:s
        condiciones.append(f"ic.fecha >= '{fecha_inicio}' AND ic.fecha <= '{fecha_fin}'")
   
    if condiciones:
        query += "WHERE "
        query += " AND ".join(condiciones)

    query += f"""
                GROUP BY c.inst_clase_id, cl.dia, cl.hora, a.nombre
                ORDER BY cancelaciones DESC
            """

    return ejecutar_fetchall(query, cursor)