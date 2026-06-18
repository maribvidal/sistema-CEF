from db.operaciones.exception_handler import ejecutar_query

def borrar_usuario_pertenece_lista_espera_abonados_por_id(id_lea: int, id_usuario: int, cursor):
    """Operación que elimina de una lista de espera, a un usuario
        que pertenecía a esa lista."""
    query = f"""DELETE FROM Usuario_Pertenece_Lista_Espera_Abonados
                WHERE lea_id = {id_lea} AND usuario_id = {id_usuario};"""
    return ejecutar_query(query, cursor)

def borrar_usuario_pertenece_lista_espera_individual_por_id(id_lei: int, id_usuario: int, cursor):
    """Operación que elimina de una lista de espera, a un usuario
        que pertenecía a esa lista."""
    query = f"""DELETE FROM Usuario_Pertenece_Lista_Espera_Individual
                WHERE lei_id = {id_lei} AND usuario_id = {id_usuario};"""
    return ejecutar_query(query, cursor)
