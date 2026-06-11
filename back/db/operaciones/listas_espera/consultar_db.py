from db.operaciones.exception_handler import ejecutar_fetchall, ejecutar_fetchone

def consultar_lista_espera_por_usuario_clase(id_usuario: int, id_clase: int, cursor):
    """Operación que consulta por listas de espera según el id del usuario y el id de la clase
        asociada a la lista de espera."""
    query = f"""
        SELECT 1
        FROM Lista_Espera_Publico_General leg
        WHERE leg.usuario_id = {id_usuario}
          AND leg.inst_clase_id = {id_clase}

        UNION

        SELECT 1
        FROM Lista_Espera_Abonados lea
        WHERE lea.usuario_id = {id_usuario}
          AND lea.inst_clase_id = {id_clase}
    """
    return ejecutar_fetchone(query, cursor);