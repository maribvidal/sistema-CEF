from db.operaciones.conectar_db import conectarse_db
from db.operaciones.commitear_db import commitear
from db.operaciones.cuentas import insertar_cuenta

def insertar_usuario(dni: int, nombre: str, apellido: str, contraseña: str, fecha_nac, correo: str, telefono: str, genero: str):
    """Permite insertar una fila para la tabla Usuario"""
    insertar_cuenta(dni, nombre, apellido, contraseña, correo, genero)
    cursor = conectarse_db()
    cursor.execute(f"""
            INSERT INTO Usuario (dni, fecha_nac, telefono)
            VALUES({dni}, '{fecha_nac}', '{telefono}');
        """)
    commitear(cursor)
