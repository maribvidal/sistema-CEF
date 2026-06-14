from db.operaciones.exception_handler import ejecutar_query 

# habria que verificar en cual de las dos tablas tiene los datos a borrar pero de todas formas tendria que funcionar.
def borrar_lista_espera(id_usuario: int, id_clase: int, cursor):
    """Permite eliminar una fila para la tabla Lista_Espera_Publico_General o Lista_Espera_Abonados"""
    query = f"""
        DELETE FROM Lista_Espera_Publico_General
        WHERE usuario_id = {id_usuario} AND inst_clase_id = {id_clase};

        DELETE FROM Lista_Espera_Abonados
        WHERE usuario_id = {id_usuario} AND clase_id = {id_clase};
    """
    return ejecutar_query(query, cursor)