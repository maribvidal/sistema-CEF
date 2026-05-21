from db.operaciones.exception_handler import ejecutar_query 

def modificar_clase_ocurrir_sala(clase_id: int, sala_id: int, fecha, hora: str, cursor):
    """Permite modificar una fila para la tabla Clase_Ocurrir_Sala"""
    query = f"""UPDATE Clase_Ocurrir_Sala
                SET sala_id = {sala_id},
                    fecha = '{fecha}',
                    hora = {hora}
                WHERE clase_id = {clase_id};"""
    return ejecutar_query(query, cursor)
