from db.operaciones.exception_handler import ejecutar_insertar

def insertar_usuario(dni: int, nombre: str, apellido: str, contraseña: str, fecha_nac: str, correo: str, telefono: str, genero: str, rol: int, cursor):
    """Permite insertar una fila para la tabla Usuario"""
    query = f"""INSERT INTO Usuario (dni, nombre, apellido, contraseña, fecha_nac, correo, telefono, genero, rol_id)
                VALUES ({dni}, '{nombre}', '{apellido}', '{contraseña}', '{fecha_nac}', '{correo}', '{telefono}', '{genero}', {rol});"""
    return ejecutar_insertar(query, cursor)
