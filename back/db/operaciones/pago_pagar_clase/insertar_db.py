from db.operaciones.commitear_db import commitear

def insertar_pago_pagar_clase(cursor, pago_id: int, clase_id: int):
    """Permite insertar una fila para la tabla Pago_Pagar_Clase"""
    query = f"""INSERT INTO Pago_Pagar_Clase (pago_id, clase_id)
                VALUES ({pago_id}, {clase_id});"""
    cursor.execute(query)
    commitear(cursor)
    return cursor.lastrowid
