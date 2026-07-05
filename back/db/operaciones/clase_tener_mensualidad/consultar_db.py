from db.operaciones.exception_handler import ejecutar_fetchall, ejecutar_fetchone

def consultar_montos_mensualidad(id_mensualidad: int, cursor) -> dict:
    """Hace una consulta para obtener los montos de una mensualidad por su ID, y devuelve una tupla con los datos de la mensualidad"""
    return ejecutar_fetchone(f"""
            SELECT SUM(c.monto) as total
            FROM Clase_Tener_Mensualidad cm 
            INNER JOIN Mensualidad m ON cm.mensualidad_id = m.id
            INNER JOIN Clase c ON cm.clase_id = c.id
            INNER JOIN Instancia_Clase ic ON c.id = ic.clase_id
            WHERE m.id = {id_mensualidad} and ic.fecha >= DATE('now') AND ic.fecha BETWEEN m.fecha_ini AND m.fecha_fin 
        """, cursor)