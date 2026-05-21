from db.operaciones.commitear_db import commitear

def insertar_descuento(nombre: str, cursor):
    """Permite insertar una fila para la tabla Descuento"""
    query = f"""INSERT INTO Descuento (nombre)
                VALUES ('{nombre}');"""
    return ejecutar_insertar(query, cursor)
