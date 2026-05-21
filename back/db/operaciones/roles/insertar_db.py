from db.operaciones.commitear_db import commitear

def insertar_rol(nombre: str, cursor):
    """Permite insertar una fila para la tabla Rol"""
    query = f"""INSERT INTO Rol (nombre) 
                VALUES ('{nombre}');"""
    ejecutar_insertar(query, cursor)
