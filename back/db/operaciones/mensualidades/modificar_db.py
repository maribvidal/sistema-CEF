from db.operaciones.exception_handler import ejecutar_query 

def configurar_fin_mensualidad(id_mensualidad: int, cursor, fecha_fin=None):
    """Permite configurar la fecha de fin de una mensualidad."""
    
    if fecha_fin is not None:  # 👈 condición corregida
        seteo = f"SET fecha_fin = '{fecha_fin}' "  # 👈 espacio al final
    else:
        seteo = "SET fecha_fin = (DATETIME(fecha_fin, '+1 month')) "  # 👈 espacio al final
        
    query = f"UPDATE Mensualidad {seteo}WHERE id = {id_mensualidad};"
    return ejecutar_query(query, cursor)

def cancelar_mensualidad(id_mensualidad: int, cursor):
    """Permite cancelar una mensualidad."""
    query = f"""UPDATE Mensualidad SET estado = 1 WHERE id = {id_mensualidad};"""
    return ejecutar_query(query, cursor)