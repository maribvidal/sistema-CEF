from db.operaciones.exception_handler import ejecutar_insertar 

def insertar_empleado(nombre: str, apellido: str, correo: str, contraseña: str, genero: str, dni: int, rol_id: int, cursor):
    """Permite insertar una fila para la tabla Empleado"""
    query = f"""INSERT INTO Empleado (nombre, apellido, correo, contraseña, genero, dni, rol_id)
                VALUES ('{nombre}', '{apellido}', '{correo}', '{contraseña}', '{genero}', {dni}, {rol_id});"""
    ejecutar_insertar(query, cursor)
