from db.operaciones.exception_handler import ejecutar_insertar

def registrar_asistencia(id_usuario: int, id_clase: int, cursor):
    """Permite insertar una fila para la tabla Asistencia"""
    query = f"""INSERT INTO Asistencias_Clase (usuario_id, con_mensualidad, inst_clase_id)
                VALUES ({id_usuario}, 1, {id_clase});"""
    return ejecutar_insertar(query, cursor)