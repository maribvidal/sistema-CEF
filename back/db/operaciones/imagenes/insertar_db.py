from db.operaciones.exception_handler import ejecutar_insertar

def insertar_imagen(contenido: bytes, cursor):
    """Permite insertar una fila para la tabla Imagen"""
    query = f"INSERT INTO Imagen (contenido) VALUES ('{contenido}');"
    return ejecutar_insertar(query, cursor)
