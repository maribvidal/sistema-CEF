from db.operaciones.exception_handler import ejecutar_insertar

def insertar_profesor(nombre: str, apellido: str, genero: str, dni: int, cursor):
    """Permite insertar una fila para la tabla Profesor"""
    query = f"""INSERT INTO Usuario (nombre, apellido, genero, dni, rol_id)
                VALUES('{nombre}', '{apellido}', '{genero}', '{dni}', 5);"""
    return ejecutar_insertar(query, cursor)
