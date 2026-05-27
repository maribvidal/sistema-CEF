from db.operaciones.exception_handler import ejecutar_insertar

def insertar_sala(nombre: str, capacidad: int, cursor):
    """Permite insertar una fila para la tabla Sala"""
    query = f"""INSERT INTO Sala (nombre, capacidad)
                VALUES ('{nombre}', {capacidad});"""
    ejecutar_insertar(query, cursor)
