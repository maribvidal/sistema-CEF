from db.operaciones.commitear_db import commitear

def insertar_pago(monto: float, usuario_id: int, cursor):
    """Permite insertar una fila para la tabla Pago"""
    query = f"""INSERT INTO Pago (monto, usuario_id)
                VALUES ({monto}, {usuario_id});"""
    ejecutar_insertar(query, cursor)
