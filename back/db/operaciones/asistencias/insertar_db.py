from db.operaciones.exception_handler import ejecutar_insertar

def registrar_asistencia(id_usuario: int, id_clase: int, cursor):
    """Permite insertar una fila para la tabla Asistencia"""
    query = f"""INSERT INTO Asistencia (usuario_id, inst_clase_id)
                VALUES ({id_usuario}, {id_clase});"""
    return ejecutar_insertar(query, cursor)