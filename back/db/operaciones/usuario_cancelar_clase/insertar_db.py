from db.operaciones.conectar_db import conectarse_db
from db.operaciones.commitear_db import commitear

def insertar_usuario_cancelar_clase(usuario_id: int, clase_id: int):
    """Permite insertar una fila para la tabla Usuario_Cancelar_Clase"""
    query = f"""INSERT INTO Usuario_Cancelar_Clase (usuario_id, clase_id)
                VALUES ({usuario_id}, {clase_id});"""
    cursor = conectarse_db()
    cursor.execute(query)
    commitear(cursor)
