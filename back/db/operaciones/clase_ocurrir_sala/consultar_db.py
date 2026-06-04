from db.operaciones.exception_handler import ejecutar_fetchone, ejecutar_fetchall

def consultar_clase_ocurrir_sala_por_dia_hora_sala(sala_id, dia, hora, cursor):
    """Función que consulta la clase_ocurrir_sala por dia, hora y sala"""
    query = f"""
        SELECT clase_id, sala_id, dia, hora
        FROM Clase_Ocurrir_Sala
        WHERE sala_id = {sala_id} AND dia = '{dia}' AND hora = '{hora}'
    """

    return ejecutar_fetchone(query, cursor)

def consultar_clase_ocurrir_sala_por_claseid_dia_hora(clase_id, dia, hora, cursor):
    """Función que consulta la clase_ocurrir_sala por el id de la clase, el día
        y la hora."""
    query = f"""
        SELECT id, clase_id, sala_id, dia, hora
        FROM Clase_Ocurrir_Sala
        WHERE clase_id = {clase_id} AND dia = '{dia}' AND hora = '{hora}'
    """

    return ejecutar_fetchone(query, cursor)

def consultar_usuarios_inscriptos_clase_ocurrir_sala(clase_ocu_sala_id, cursor):
    """Función que, dado un id de clase_ocurrir_sala, retorna todas
        las tuplas que encuentre de gente inscripta en dicha clase."""
    query = f"""
        SELECT *
        FROM Usuario_Inscribir_Clase uic
            INNER JOIN Clase_Ocurrir_Sala cos ON (uic.clase_ocurrir_sala_id = cos.id)
        WHERE cos.id = {clase_ocu_sala_id}
    """
    
    return ejecutar_fetchall(query, cursor)
