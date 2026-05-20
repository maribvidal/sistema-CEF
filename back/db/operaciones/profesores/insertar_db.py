from db.operaciones.exception_handler import ejecutar_insertar 

def insertar_profesor(nombre: str, apellido: str, genero: str, dni: int, cursor):
    """Permite insertar una fila para la tabla Profesor"""
    query = f"""INSERT INTO Profesor (nombre, apellido, genero, dni)
                VALUES('{nombre}', '{apellido}', '{genero}', '{dni}');"""
    ejecutar_insertar(query, cursor)
