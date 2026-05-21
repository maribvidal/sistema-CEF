from db.operaciones.exception_handler import ejecutar_insertar

def insertar_sala(nombre: str, cursor):
    """Permite insertar una fila para la tabla Sala"""
    query = f"""INSERT INTO Sala (nombre)
                VALUES ('{nombre}');"""
    ejecutar_insertar(query, cursor)
