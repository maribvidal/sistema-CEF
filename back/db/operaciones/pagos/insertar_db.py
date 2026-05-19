from db.operaciones.conectar_db import conectarse_db
from db.operaciones.commitear_db import commitear

def insertar_pago(monto: float, usuario_id: int):
    """Permite insertar una fila para la tabla Pago"""
    cursor = conectarse_db()
    cursor.execute(f"""INSERT INTO Pago (monto, usuario_id)
                                VALUES ({monto}, {usuario_id});""")
    commitear(cursor)
