from db.operaciones.exception_handler import ejecutar_fetchall, ejecutar_fetchone

def consultar_usuario_inscribir_clase_por_usuario_id(usuario_id: int, clase_id: int, cursor):
    """Permite consultar si el usuario se ha inscrito en la clase, buscando por usuario_id y clase_id"""
    query = f"""SELECT * FROM Usuario_Inscribir_Clase WHERE usuario_id = {usuario_id} AND clase_id = {clase_id};"""
    return ejecutar_fetchone(query, cursor)

def consultar_superposicion_horaria_clase_usuario(usuario_id: int, clase_id: int, cursor):
    """Permite consultar si el usuario tiene una clase que se superpone con la clase a inscribir"""
    query = f"""
        SELECT 1
        FROM Usuario_Inscribir_Clase uic
        INNER JOIN Clase_Ocurrir_Sala cos 
            ON cos.clase_id = uic.clase_id
        WHERE uic.usuario_id = {usuario_id}
          AND cos.fecha = (
              SELECT cos2.fecha
              FROM Clase_Ocurrir_Sala cos2
              WHERE cos2.clase_id = {clase_id}
          )
          AND cos.hora = (
              SELECT cos3.hora
              FROM Clase_Ocurrir_Sala cos3
              WHERE cos3.clase_id = {clase_id}
          )
    """
    return ejecutar_fetchall(query, cursor)