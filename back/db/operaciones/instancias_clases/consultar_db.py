from db.operaciones.exception_handler import ejecutar_fetchone, ejecutar_fetchall

def consultar_instancia_clase_por_id(ins_id, cursor) -> dict:
    """Hace una consulta para obtener una instancia de clase por su ID, y devuelve una tupla."""
    return ejecutar_fetchone(f"SELECT * FROM Instancia_Clase WHERE id = {ins_id}", cursor)

def consultar_instancia_clase_por_clase_id(clase_id, cursor) -> dict:
    """Hace una consulta para obtener una instancia de clase por su clase_id, y devuelva tuplas."""
    return ejecutar_fetchall(f"SELECT * FROM Instancia_Clase WHERE clase_id = {clase_id}", cursor)

def obtener_reservas_instancia_clase(ins_id, cursor) -> dict:
    """Hace una consulta para devolver todas las reservas que tengan un mismo inst_clase_id."""
    return ejecutar_fetchall(f"SELECT * FROM Reserva WHERE inst_clase_id = {ins_id}", cursor)

def listar_instancias_clases_semana(cursor) -> dict:
    """Hace una consulta para devolver todas las instancias de la clase que ocurran
        en la semana de la fecha."""
    query = f"""
                SELECT id, fecha, clase, monto
                FROM Instancia_Clase
                WHERE fecha BETWEEN DATE('now') AND DATE('now', 'weekday 6')
    """
    return ejecutar_fetchall(query, cursor)

def obtener_instancia_clase_por_clase_id_semana(clase_id: int, cursor) -> dict:
    """Hace una consulta para devolver la instancia de clase para un clase_id
        y una fecha."""
    query = f"""
                SELECT *
                FROM Instancia_Clase
                WHERE fecha BETWEEN DATE('now') AND DATE('now', 'weekday 6') AND clase_id = {clase_id}
            """
    return ejecutar_fetchone(query, cursor)

def revisar_validez_cupos(dict_cupos: dict, cursor, fecha_fin_mensualidad = None):
    dict_cupos_validos = {}
    for key in dict_cupos.keys():
        query = f"""
            SELECT 1 
            FROM Instancia_Clase ic
            WHERE ic.id = {key} AND ic.fecha BETWEEN DATE('now') 
        """
        if fecha_fin_mensualidad is not None:
            # query += f""" AND DATE('{fecha_fin_mensualidad}', '+10 days')"""
            query += f""" AND DATE('{fecha_fin_mensualidad}', '+1 month')"""
        else:
            # query += f""" AND DATE('now', '+1 month')"""
            query += f""" AND DATE('now', '+2 month')"""
        
        resultado = ejecutar_fetchone(query, cursor)
        if resultado['status'] == "success" and resultado['data'] is not None:
            dict_cupos_validos[key] = dict_cupos[key]
    
    return dict_cupos_validos