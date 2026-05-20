from db.operaciones.exception_handler import ejecutar_insertar 

def insertar_recepcionista(dni: int, cursor):
    """Permite insertar una fila para la tabla Recepcionista"""
    query = f"""INSERT INTO Recepcionista (dni)
                VALUES ({dni});"""
    ejecutar_insertar(query, cursor)
