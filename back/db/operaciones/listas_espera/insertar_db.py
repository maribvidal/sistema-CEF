from db.operaciones.exception_handler import ejecutar_insertar

def anotarse_lista_publico_general(id_usuario: int, id_clase: int, cursor):
    """Permite insertar una fila para la tabla Lista_Espera_Publico_General"""
    query = f"""INSERT INTO Lista_Espera_Publico_General (usuario_id, inst_clase_id)
                VALUES ({id_usuario}, {id_clase});"""
    return ejecutar_insertar(query, cursor)

def insertar_lista_espera_abonados(id_clase: int, cursor):
    """Permite insertar una fila para la tabla Lista_Espera_Abonados"""
    query = f"""INSERT INTO Lista_Espera_Abonados (clase_id)
        VALUES ({id_clase});"""
    return ejecutar_insertar(query, cursor)

def insertar_lista_espera_individual(id_ins_clase: int, cursor):
    """Permite insertar una fila para la tabla Lista_Espera_Abonados"""
    query = f"""INSERT INTO Lista_Espera_Individual (inst_clase_id)
        VALUES ({id_ins_clase});"""
    return ejecutar_insertar(query, cursor)
