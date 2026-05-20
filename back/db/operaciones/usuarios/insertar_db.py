from db.operaciones.cuentas import insertar_cuenta
from db.operaciones.commitear_db import commitear

def insertar_usuario(cursor, dni: int, nombre: str, apellido: str, contraseña: str, fecha_nac: str, correo: str, telefono: str, genero: str):
    """Permite insertar una fila para la tabla Usuario"""
    insertar_cuenta(cursor, dni, nombre, apellido, contraseña, correo, genero)
    cursor.execute(f"""INSERT INTO Usuario (dni, fecha_nac, telefono)
                                VALUES({dni}, '{fecha_nac}', '{telefono}')""")
    commitear(cursor)
    return cursor.lastrowid
