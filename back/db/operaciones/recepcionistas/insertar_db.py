from db.operaciones.commitear_db import commitear

def insertar_recepcionista(dni: int, cursor):
    """Permite insertar una fila para la tabla Recepcionista"""
    query = f"""INSERT INTO Recepcionista (dni)
                VALUES ({dni});"""
    ejecutar_insertar(query, cursor)
