from db.operaciones.exception_handler import ejecutar_insertar 

def insertar_pago_pagar_mensualidad(pago_id: int, mensualidad_id: int, cursor):
    """Permite insertar una fila para la tabla Pago_Pagar_Mensualidad"""
    query = f"""INSERT INTO Pago_Pagar_Mensualidad (pago_id, mensualidad_id)
                VALUES ({pago_id}, {mensualidad_id});"""
    ejecutar_insertar(query, cursor)
