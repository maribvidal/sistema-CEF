from db.operaciones.exception_handler import ejecutar_query 

def borrar_pago(cursor, id_pago):
    """Borra un pago de la base de datos dado su ID."""
    query = f"DELETE FROM pagos WHERE id = {id_pago};"
    return ejecutar_query(cursor, query)