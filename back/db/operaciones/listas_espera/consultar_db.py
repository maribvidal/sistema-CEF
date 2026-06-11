from db.operaciones.exception_handler import ejecutar_fetchall, ejecutar_fetchone

def consultar_lista_espera_por_usuario_clase(id_usuario: int, id_clase: int, cursor):
    """Operación que consulta por listas de espera según el id del usuario y el id de la clase
        asociada a la lista de espera."""
    query = f"""
        SELECT 1
        FROM Lista_Espera_Individual leg
        WHERE leg.usuario_id = {id_usuario}
          AND leg.inst_clase_id = {id_clase}

        UNION

        SELECT 1
        FROM Lista_Espera_Abonados lea
        WHERE lea.usuario_id = {id_usuario}
          AND lea.inst_clase_id = {id_clase}
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