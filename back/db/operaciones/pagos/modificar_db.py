from db.operaciones.exception_handler import ejecutar_query 

def actualizar_estado_pago(id_pago: int, nuevo_estado: str, cursor):
    """Permite actualizar el estado de un pago en la tabla Pago."""
    query = f"""UPDATE Pago
                SET estado = '{nuevo_estado}'
                WHERE id = {id_pago};"""
    return ejecutar_query(query, cursor)