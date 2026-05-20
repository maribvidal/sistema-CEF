from db.operaciones.exception_handler import ejecutar_insertar 

def insertar_permiso(nombre: str):
    """Permite insertar una fila para la tabla Permiso"""
    query = f"""INSERT INTO Permiso (nombre)
                VALUES ('{nombre}');"""
    ejecutar_insertar(query)
