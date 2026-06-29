from db.operaciones.exception_handler import ejecutar_query 

# habria que verificar en cual de las dos tablas tiene los datos a borrar pero de todas formas tendria que funcionar.
def borrar_listas_espera_clase(id_clase: int, cursor):
    """Permite eliminar una fila para la tabla Lista_Espera_Publico_General o Lista_Espera_Abonados"""
    query = f"""
        DELETE FROM Lista_Espera_Individual
        WHERE inst_clase_id IN (SELECT id
               FROM Instancia_Clase ic INNER JOIN Clase c ON (ic.clase_id = c.id)
               WHERE c.id = {id_clase});

        DELETE FROM Lista_Espera_Abonados
        WHERE clase_id = {id_clase};
    """
    return ejecutar_query(query, cursor)
