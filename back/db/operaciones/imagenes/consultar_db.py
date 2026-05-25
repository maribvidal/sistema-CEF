from db.operaciones.exception_handler import ejecutar_fetchone

def consultar_imagen_por_id(id: int, cursor):
    """Permite consultar una fila de la tabla Imagen por su id"""
    query = f"SELECT * FROM Imagen WHERE id = {id};"
    return ejecutar_fetchone(query, cursor)

def consultar_imagen_actual_usuario(usuario_id: int, cursor):
    """Permite consultar una fila de la tabla Imagen por el id del usuario al que pertenece"""
    query = f"""
        SELECT im.contenido
        FROM Usuario u INNER JOIN Imagen im ON u.imagen_id = im.id
        WHERE u.id = {usuario_id};
    """
    return ejecutar_fetchone(query, cursor)
