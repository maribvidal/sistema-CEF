from db.operaciones.exception_handler import ejecutar_fetchall, ejecutar_fetchone

def consultar_imagen_por_id(id: int):
    """Permite consultar una fila de la tabla Imagen por su id"""
    query = f"SELECT * FROM Imagen WHERE id = {id};"
    return ejecutar_fetchone(query)
