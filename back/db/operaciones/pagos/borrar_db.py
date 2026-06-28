from db.operaciones.exception_handler import ejecutar_query 

def borrar_pago(cursor, id_pago):
    """Borra un pago de la base de datos dado su ID."""
    query = f"DELETE FROM Pago WHERE id = {id_pago};"
    return ejecutar_query(query, cursor)