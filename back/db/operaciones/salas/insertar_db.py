from db.operaciones.commitear_db import commitear

def insertar_sala(nombre: str, cursor):
    """Permite insertar una fila para la tabla Sala"""
    query = f"""INSERT INTO Sala (nombre)
                VALUES ('{nombre}');"""
    ejecutar_insertar(query, cursor)
