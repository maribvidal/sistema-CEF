from db.operaciones.exception_handler import ejecutar_query 

def configurar_fin_mensualidad(id_mensualidad: int, cursor, fecha_fin=None):
    """Permite configurar la fecha de fin de una mensualidad."""
    query = "UPDATE Mensualidad"
    
    if fecha_fin is not None:
        seteo=f""" SET fecha_fin = DATE('{fecha_fin}')"""
    else:
        seteo=f""" 
            SET
                fecha_ini = CASE
                    WHEN DATE(fecha_fin, '+10 days') < DATE('now')
                        THEN DATE('now')
                    ELSE fecha_ini
                END,
                
                fecha_fin = CASE
                    WHEN DATE(fecha_fin, '+10 days') < DATE('now')
                        THEN DATE('now', '+1 month')
                    ELSE DATE(fecha_fin, '+1 month')
                END
        """
        
    query += seteo
    query += f""" WHERE id = {id_mensualidad};"""
    
    return ejecutar_query(query, cursor)

def cancelar_mensualidad(id_mensualidad: int, cursor):
    """Permite cancelar una mensualidad."""
    query = f"""UPDATE Mensualidad SET estado = 1 WHERE id = {id_mensualidad};"""
    return ejecutar_query(query, cursor)

def configurar_datos_mensualidad(mensualidad, cursor) -> dict:
    """Hace una consulta para configurar los datos de una mensualidad"""
    query = f"""
        UPDATE Mensualidad
        SET fecha_ini = DATE('{mensualidad['fecha_ini']}'),
            fecha_fin = DATE('{mensualidad['fecha_fin']}'),
            estado = {mensualidad['estado']}
        WHERE id = {mensualidad['id']}
    """
    return ejecutar_query(query, cursor)