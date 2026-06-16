from db.operaciones.exception_handler import ejecutar_fetchall, ejecutar_fetchone

def consultar_lista_espera_abonado(id_usuario: int, id_clase: int, cursor):
    """Operación que consulta por listas de espera según el id del usuario y el id de la clase
        asociada a la lista de espera."""
    query = f"""
        SELECT 1
        FROM Lista_Espera_Abonados lea
        WHERE lea.usuario_id = {id_usuario}
          AND lea.clase_id = {id_clase}
    """
    return ejecutar_fetchone(query, cursor);
  
def consultar_lista_espera_individual(id_usuario: int, id_clase: int, cursor):
    """Operación que consulta por listas de espera según el id del usuario y el id de la clase
        asociada a la lista de espera."""
    query = f"""
        SELECT 1
        FROM Lista_Espera_Individual lei
        WHERE lei.usuario_id = {id_usuario}
          AND lei.inst_clase_id = {id_clase}
    """
    return ejecutar_fetchone(query, cursor);
  
def obtener_siguiente_usuario_abonado(id_clase: int, cursor):
    """Operación que obtiene al siguiente usuario en la lista de espera de una clase."""
    query = f"""
        SELECT u.correo
        FROM Lista_Espera_Abonados l
        INNER JOIN Usuarios u ON l.usuario_id = u.id
        WHERE l.inst_clase_id = {id_clase}
        ORDER BY l.fecha ASC
        LIMIT 1
    """
    return ejecutar_fetchone(query, cursor);
  
def obtener_siguiente_usuario_individual(id_clase: int, cursor):
    """Operación que obtiene al siguiente usuario en la lista de espera de una clase."""
    query = f"""
        SELECT u.correo
        FROM Lista_Espera_Individual l
        INNER JOIN Usuarios u ON l.usuario_id = u.id
        WHERE l.inst_clase_id = {id_clase}
        ORDER BY l.fecha ASC
        LIMIT 1
    """
    return ejecutar_fetchone(query, cursor);

def obtener_lista_espera_abonados_por_id_clase(id_clase: int, cursor):
    """Operaión que obtiene una lista de espera de abonados por el
        id de la clase a la cual está asociada."""
    query = f"""
        SELECT id
        FROM Lista_Espera_Abonados
        WHERE clase_id = {id_clase};
    """
    return ejecutar_fetchone(query, cursor)

def obtener_usuarios_lista_espera_abonados(id_lea: int, cursor):
    """Operación que obtiene todos los usuarios que pertenecen a
        una lista de espera de abonados. Requiere el id de esta."""
    query = f"""
        SELECT *
        FROM Usuario_Pertenece_Lista_Espera_Abonados
        WHERE lea_id = {id_lea};
    """
    return ejecutar_fetchall(query, cursor)

def obtener_lista_espera_individual_por_id_ins_clase(id_ins_clase: int, cursor):
    """Operaión que obtiene una lista de espera individual por el
        id de la instancia de la clase a la cual está asociada."""
    query = f"""
        SELECT id
        FROM Lista_Espera_Individual
        WHERE inst_clase_id = {id_ins_clase};
    """
    return ejecutar_fetchone(query, cursor)

def obtener_usuarios_lista_espera_individual(id_lei: int, cursor):
    """Operación que obtiene todos los usuarios que pertenecen a
        una lista de espera individual. Requiere el id de esta."""
    query = f"""
        SELECT *
        FROM Usuario_Pertenece_Lista_Espera_Individual
        WHERE lei_id = {id_lei};
    """
    return ejecutar_fetchall(query, cursor)
