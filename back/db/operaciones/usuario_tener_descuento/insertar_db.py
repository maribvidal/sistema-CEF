from db.operaciones.conectar_db import conectarse_db
from db.operaciones.commitear_db import commitear

def insertar_usuario_tener_descuento(usuario_id: int, descuento_id: int):
    """Permite insertar una fila para la tabla Usuario_Tener_Descuento"""
    cursor = conectarse_db()
    cursor.execute(f"""INSERT INTO Usuario_Tener_Descuento (usuario_id, descuento_id)
                                VALUES ({usuario_id}, {descuento_id});""")
    commitear(cursor)
