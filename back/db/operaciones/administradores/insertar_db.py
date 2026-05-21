from db.operaciones.exception_handler import ejecutar_insertar 

def insertar_administrador(dni: int, cursor):
    """Permite insertar una fila para la tabla Administrador"""
    query = f"""INSERT INTO Administrador (dni)
                VALUES ({dni});"""
    return ejecutar_insertar(query, cursor)
