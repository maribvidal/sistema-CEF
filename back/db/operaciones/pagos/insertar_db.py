from db.operaciones.exception_handler import ejecutar_insertar

def insertar_pago(monto: float, usuario_id: int, cursor):
    """Permite insertar una fila para la tabla Pago"""
    query = f"""INSERT INTO Pago (monto, fecha, estado, usuario_id)
                VALUES ({monto}, (date('now')), 'pending', {usuario_id});"""
    return ejecutar_insertar(query, cursor)
