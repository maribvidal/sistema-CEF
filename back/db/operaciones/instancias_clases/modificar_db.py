from db.operaciones.exception_handler import ejecutar_query

def modificar_instancias_clases_montos_proximo_mes_por_clase(id_clase: int, monto, cursor):
    """ Operación que permite modificar todos los montos de las instancias de una
        clase pasada por argumento."""
    query = f"""
        UPDATE Instancia_Clase
        SET monto = {monto}
        WHERE id IN (
            SELECT ic.id
            FROM Instancia_Clase ic
            WHERE ic.clase_id = {id_clase} AND  
                DATE('ic.fecha') > DATE('now', 'start of month', '+1 month')
        );
    """
    return ejecutar_query(query, cursor)
