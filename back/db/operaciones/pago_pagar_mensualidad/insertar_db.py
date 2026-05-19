from db.operaciones.conectar_db import conectarse_db
from db.operaciones.commitear_db import commitear

def insertar_pago_pagar_mensualidad(pago_id: int, mensualidad_id: int):
    """Permite insertar una fila para la tabla Pago_Pagar_Mensualidad"""
    cursor = conectarse_db()
    cursor.execute(f"""INSERT INTO Pago_Pagar_Mensualidad (pago_id, mensualidad_id)
                                VALUES ({pago_id}, {mensualidad_id});""")
    commitear(cursor)
