from db.operaciones.exception_handler import ejecutar_fetchall, ejecutar_fetchone

def consultar_mensualidad_por_pago_id(pago_id: int, cursor):
    query = f"""
        SELECT mensualidad_id
        FROM Pago_Pagar_Mensualidad
        WHERE pago_id = {pago_id}
    """
    return ejecutar_fetchone(query, cursor)
