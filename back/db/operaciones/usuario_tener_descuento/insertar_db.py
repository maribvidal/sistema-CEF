from db.operaciones.exception_handler import ejecutar_insertar

def insertar_usuario_tener_descuento(usuario_id: int, descuento_id: int, cursor):
    """Permite insertar una fila para la tabla Usuario_Tener_Descuento"""
    query = f"""INSERT INTO Usuario_Tener_Descuento (usuario_id, descuento_id)
                VALUES ({usuario_id}, {descuento_id});"""
    ejecutar_insertar(query, cursor)
