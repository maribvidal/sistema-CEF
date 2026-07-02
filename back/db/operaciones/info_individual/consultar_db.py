from db.operaciones.exception_handler import ejecutar_fetchone

def obtener_info_individual_por_pago_id(pago_id, cursor):
    query = f"SELECT * FROM Info_Individual WHERE pago_id = {pago_id}"
    return ejecutar_fetchone(query, cursor)
