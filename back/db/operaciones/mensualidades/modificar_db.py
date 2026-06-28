from db.operaciones.exception_handler import ejecutar_query 

def configurar_fin_mensualidad(id_mensualidad: int, cursor, fecha_fin = None):
    """Permite configurar la fecha de fin de una mensualidad."""
    query = f"""UPDATE Mensualidad"""
    
    if fecha_fin is None:
        seteo=f"""SET fecha_fin = '{fecha_fin}'"""
    else:
        seteo=f"""SET fecha_fin = (DATETIME(fecha_fin, '+1 month'))"""
        
    query += seteo
    query += f"""WHERE id = {id_mensualidad};"""
    return ejecutar_query(query, cursor)

def cancelar_mensualidad(id_mensualidad: int, cursor):
    """Permite cancelar una mensualidad."""
    query = f"""UPDATE Mensualidad SET estado = 1 WHERE id = {id_mensualidad};"""
    return ejecutar_query(query, cursor)