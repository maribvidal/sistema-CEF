from db.operaciones.exception_handler import ejecutar_insertar

def insertar_pago_pagar_clase(pago_id: int, clase_id: int, cursor):
    """Permite insertar una fila para la tabla Pago_Pagar_Clase"""
    query = f"""INSERT INTO Pago_Pagar_Clase (pago_id, clase_id)
                VALUES ({pago_id}, {clase_id});"""
    ejecutar_insertar(query, cursor)
