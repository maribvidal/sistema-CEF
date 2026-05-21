from db.operaciones.commitear_db import commitear

def insertar_actividad(nombre: str, precio_mensual: float, cursor):
    """Permite insertar una fila para la tabla Actividad"""
    query = f"""INSERT INTO Actividad (nombre, precio_mensual)
                VALUES ('{nombre}', {precio_mensual});"""
    return ejecutar_insertar(query, cursor)
