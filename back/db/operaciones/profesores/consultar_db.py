from db.operaciones.exception_handler import ejecutar_fetchall, ejecutar_fetchone

def consultar_profesor_por_id(id: int, cursor) -> dict:
    """Hace una consulta para devolver la tupla de un profesor por su id."""
    return ejecutar_fetchone(f"SELECT * FROM Usuario WHERE rol_id = 5 AND id = {id};", cursor)

def listar_profesores(cursor) -> dict:
    """Hace una consulta para listar todos los profesores, y devuelve una lista de tuplas"""
    return ejecutar_fetchall("SELECT * FROM Usuario WHERE rol_id = 5", cursor)

def listar_dnis_profesores(cursor) -> dict:
    """Hace una consulta para listar todos los dnis de los
        profesores, y devuelve una lista de tuplas."""
    return ejecutar_fetchall("SELECT dni FROM Usuario WHERE rol_id = 5", cursor)

# def consultar_profesor_actividad(id_profesor: int, id_actividad: int, cursor):
#     """
#     Verifica si el profesor tiene asignada la aptitud para dar una actividad.
#     Requiere que exista la tabla intermedia 'Profesor_Actividad'.
#     """
#     query = """
#         SELECT 1 
#         FROM Profesor_Actividad 
#         WHERE profesor_id = ? AND actividad_id = ?
#     """
#     cursor.execute(query, (id_profesor, id_actividad))
#     resultado = cursor.fetchone()
#     
#     # Si devuelve algo, es porque existe el registro (es apto). Si es None, no lo es.
#     return resultado is not None