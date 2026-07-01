from db.operaciones.exception_handler import ejecutar_fetchall, ejecutar_fetchone

def consultar_lista_espera_abonado_usuario_por_idClase(idClase: int, usuario_id: int, cursor):
    """Operación que consulta si un usuario pertenece a la lista de espera de abonados de una clase específica."""
    query = f"""
        SELECT 1
        FROM Lista_Espera_Abonados l
        INNER JOIN Usuario_Pertenece_Lista_Espera_Abonados up ON l.id = up.lea_id
        INNER JOIN Usuario u ON up.usuario_id = u.id
        WHERE l.clase_id = {idClase}
        AND u.id = {usuario_id};
    """
    return ejecutar_fetchone(query, cursor);

def consultar_lista_espera_individual_usuario_por_idInstanciaClase(idInstanciaClase: int, dniUsuario: int, cursor):
    """Operación que consulta si un usuario pertenece a la lista de espera individual de una instancia de clase específica."""
    query = f"""
        SELECT 1
        FROM Lista_Espera_Individual l
        INNER JOIN Usuario_Pertenece_Lista_Espera_Individual up ON l.id = up.lei_id
        INNER JOIN Usuario u ON up.usuario_id = u.id
        WHERE l.inst_clase_id = {idInstanciaClase}
        AND u.dni = {dniUsuario};
    """
    return ejecutar_fetchone(query, cursor);

def consultar_lista_espera_individual_usuario_por_ClaseID(clase_id: int, usuario_id: int, cursor):
    """Operación que consulta si un usuario pertenece a la lista de espera individual de una clase específica."""
    query = f"""
        SELECT 1
        FROM Lista_Espera_Individual l
        INNER JOIN Instancia_Clase ic ON l.inst_clase_id = ic.id
        INNER JOIN Usuario_Pertenece_Lista_Espera_Individual up ON l.id = up.lei_id
        INNER JOIN Usuario u ON up.usuario_id = u.id
        WHERE ic.clase_id = {clase_id}
        AND u.id = {usuario_id};
    """
    return ejecutar_fetchone(query, cursor);

def consultar_lista_espera_abonado(id_usuario: int, id_lea: int, cursor):
    """Operación que consulta por listas de espera según el id del usuario y el id de la clase
        asociada a la lista de espera."""
    query = f"""
        SELECT 1
        FROM Lista_Espera_Abonados l
        INNER JOIN Usuario_Pertenece_Lista_Espera_Abonados up ON l.id = up.lea_id
        WHERE up.usuario_id = {id_usuario}
          AND l.id = {id_lea}
    """
    return ejecutar_fetchone(query, cursor);
  
def consultar_lista_espera_individual(id_usuario: int, id_lei: int, cursor):
    """Operación que consulta por listas de espera según el id del usuario y el id de la clase
        asociada a la lista de espera."""
    query = f"""
        SELECT 1
        FROM Lista_Espera_Individual lei
        INNER JOIN Usuario_Pertenece_Lista_Espera_Individual up ON lei.id = up.lei_id
        WHERE up.usuario_id = {id_usuario}
          AND lei.id = {id_lei}
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

def obtener_lista_espera_individual_por_id_clase(id_clase: int, cursor):
    """Operaión que obtiene una lista de espera individual por el
        id de la clase a la cual está asociada."""
    query = f"""
        SELECT id
        FROM Lista_Espera_Individual
        WHERE inst_clase_id = {id_clase};
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
