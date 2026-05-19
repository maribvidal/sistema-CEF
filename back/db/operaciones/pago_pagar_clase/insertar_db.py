from db.operaciones.conectar_db import conectarse_db
from db.operaciones.commitear_db import commitear

def insertar_pago_pagar_clase(pago_id: int, clase_id: int):
    """Permite insertar una fila para la tabla Pago_Pagar_Clase"""
    cursor = conectarse_db()
    cursor.execute(f"""INSERT INTO Pago_Pagar_Clase (pago_id, clase_id)
                                VALUES ({pago_id}, {clase_id});""")
    commitear(cursor)
