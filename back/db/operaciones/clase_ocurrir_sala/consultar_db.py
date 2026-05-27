from db.operaciones.exception_handler import ejecutar_fetchone

def consultar_clase_ocurrir_sala_por_fecha_hora_sala(sala_id, fecha, hora, cursor):
    """Función que consulta la clase_ocurrir_sala por fecha, hora y sala"""
    query = f"""
        SELECT clase_id, sala_id, fecha, hora
        FROM Clase_Ocurrir_Sala
        WHERE sala_id = {sala_id} AND fecha = '{fecha}' AND hora = '{hora}'
    """

    return ejecutar_fetchone(query, cursor)

def consultar_clase_ocurrir_sala_por_claseid_fecha_hora(clase_id, fecha, hora, cursor):
    """Función que consulta la clase_ocurrir_sala por el id de la clase, la fecha
        y la hora."""
    query = f"""
        SELECT id, clase_id, sala_id, fecha, hora
        FROM Clase_Ocurrir_Sala
        WHERE clase_id = {clase_id} AND fecha = '{fecha}' AND hora = '{hora}'
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
