from db.operaciones.conectar_db import conectarse_db
from db.operaciones.commitear_db import commitear

def insertar_usuario(dni: int, nombre: str, apellido: str, contraseña: str, fecha_nac, correo: str, telefono: str, genero: str):
    """Permite insertar una fila para la tabla Usuario"""
    cursor = conectarse_db()
    cursor.execute(f"""INSERT INTO Usuario (dni, nombre, apellido, contraseña, fecha_nac, correo, telefono, genero)
                                VALUES({dni}, '{nombre}', '{apellido}', '{contraseña}', '{fecha_nac}', '{correo}', '{telefono}', '{genero}');""")
    commitear(cursor)
