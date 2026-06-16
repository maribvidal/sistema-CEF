from db.operaciones.exception_handler import ejecutar_query

def modificar_clase_estado(clase_id: int, estado: str, cursor):
    """Permite modificar el estado de una clase."""
    query = f"""UPDATE Clase
                SET estado = '{estado}'
                WHERE id = {clase_id};"""
    return ejecutar_query(query, cursor)

# respuesta = modificar_clase(clase_id, estado, id_actividad, id_profesor, sala, fecha, hora, cupo_maximo, cursor)
def modificar_clase(clase_id: int, estado: str, id_actividad: int, id_profesor: int, sala_id: int, dia: str, hora: str, cupo_maximo: int, cursor):
    """Permite modificar los detalles de una clase."""
    query = f"""UPDATE Clase
                SET estado = '{estado}',
                    actividad_id = {id_actividad},
                    profesor_id = {id_profesor},
                    sala_id = {sala_id},
                    dia = '{dia}',
                    hora = '{hora}',
                    cupo_maximo = {cupo_maximo}
                WHERE id = {clase_id};"""
    return ejecutar_query(query, cursor)
