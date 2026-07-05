from db.operaciones.exception_handler import ejecutar_query 

def borrar_pago_pagar_mensualidad(id_pago, id_mensualidad, cursor):
    query = f"DELETE FROM Pago_Pagar_Mensualidad WHERE pago_id = {id_pago} AND mensualidad_id = {id_mensualidad};"
    return ejecutar_query(query, cursor)