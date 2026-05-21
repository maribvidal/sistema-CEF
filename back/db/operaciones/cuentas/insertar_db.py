from db.operaciones.exception_handler import ejecutar_insertar 

def insertar_cuenta(dni: int, nombre: str, apellido: str, contraseña: str, correo: str, genero: str, cursor) -> int:
    """Función que inserta una nueva cuenta en la base de datos."""
    query = f"""INSERT INTO Cuenta (dni, nombre, apellido, contraseña, correo, genero)
                VALUES ({dni}, '{nombre}', '{apellido}', '{contraseña}', '{correo}', '{genero}');"""
    return ejecutar_insertar(query, cursor)
