from db.operaciones.exception_handler import ejecutar_query 

def borrar_pago_pagar_clase(id_pago, cursor):
    query = f"DELETE FROM Pago_Pagar_Clase WHERE pago_id = {id_pago};"
    return ejecutar_query(query, cursor)