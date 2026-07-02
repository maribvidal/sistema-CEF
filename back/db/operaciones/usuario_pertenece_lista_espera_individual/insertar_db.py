from db.operaciones.exception_handler import ejecutar_insertar

def insertar_usuario_pertenece_lista_espera_individual(usuario_id: int, lista_espera_individual_id: int, cursor):
    """Permite insertar una fila para la tabla Usuario_Pertenece_Lista_Espera_Individual"""
    query = f"""INSERT INTO Usuario_Pertenece_Lista_Espera_Individual (usuario_id, lei_id, fecha)
                VALUES ({usuario_id}, {lista_espera_individual_id}, DATE('now'));"""
    print(query)
    return ejecutar_insertar(query, cursor)