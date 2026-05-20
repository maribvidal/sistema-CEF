from db.operaciones.commitear_db import commitear

def insertar_pago_pagar_mensualidad(cursor, pago_id: int, mensualidad_id: int):
    """Permite insertar una fila para la tabla Pago_Pagar_Mensualidad"""
    query = f"""INSERT INTO Pago_Pagar_Mensualidad (pago_id, mensualidad_id)
                VALUES ({pago_id}, {mensualidad_id});"""
    cursor.execute(query)
    commitear(cursor)
    return cursor.lastrowid
