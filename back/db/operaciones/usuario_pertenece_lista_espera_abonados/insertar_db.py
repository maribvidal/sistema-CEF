from db.operaciones.exception_handler import ejecutar_insertar

def insertar_usuario_pertenece_lista_espera_abonados(usuario_id: int, lista_espera_abonados_id: int, cursor):
    """Permite insertar una fila para la tabla Usuario_Pertenece_Lista_Espera_Abonados"""
    query = f"""INSERT INTO Usuario_Pertenece_Lista_Espera_Abonados (usuario_id, lea_id, fecha)
                VALUES ({usuario_id}, {lista_espera_abonados_id}, DATE('now'));"""
    return ejecutar_insertar(query, cursor)