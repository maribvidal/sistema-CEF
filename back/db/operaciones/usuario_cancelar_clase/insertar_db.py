from db.operaciones.commitear_db import commitear

def insertar_usuario_cancelar_clase(usuario_id: int, clase_id: int, cursor):
    """Permite insertar una fila para la tabla Usuario_Cancelar_Clase"""
    query = f"""INSERT INTO Usuario_Cancelar_Clase (usuario_id, clase_id)
                VALUES ({usuario_id}, {clase_id});"""
    ejecutar_insertar(query, cursor)
