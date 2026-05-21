from db.operaciones.cuentas import insertar_cuenta
from db.operaciones.exception_handler import ejecutar_insertar

def insertar_usuario(dni: int, nombre: str, apellido: str, contraseña: str, fecha_nac: str, correo: str, telefono: str, genero: str, cursor):
    """Permite insertar una fila para la tabla Usuario"""
    insertar_cuenta(dni, nombre, apellido, contraseña, correo, genero, cursor)
    query = f"""INSERT INTO Cuenta (dni, nombre, apellido, contraseña, fecha_nac, correo, telefono, genero)
                VALUES ({dni}, '{nombre}', '{apellido}', '{contraseña}', '{fecha_nac}', '{correo}', '{telefono}', '{genero}');"""
    return ejecutar_insertar(query, cursor)