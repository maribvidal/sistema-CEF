from db.operaciones.exception_handler import ejecutar_fetchall, ejecutar_fetchone

def consultar_usuario_inscribir_clase_por_usuario_id(usuario_id: int, clase_id: int, cursor):
    """Permite consultar si el usuario se ha inscrito en la clase, buscando por usuario_id y clase_id"""
    query = f"""SELECT * FROM Usuario_Inscribir_Clase WHERE usuario_id = {usuario_id} AND clase_id = {clase_id};"""
    return ejecutar_fetchone(query, cursor)

def consultar_usuario_inscribir_clase_por_clase_ocurrir_sala_id(clase_ocurrir_sala_id: int, cursor):
    """Permite obtener las filas de una clase en particular
        a partir del clase_ocurrir_sala_id."""
    query = f"""SELECT * FROM Usuario_Inscribir_Clase WHERE clase_ocurrir_sala_id = {clase_ocurrir_sala_id}"""
    return ejecutar_fetchall(query, cursor)
