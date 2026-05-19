from db.operaciones.conectar_db import conectarse_db
from db.operaciones.commitear_db import commitear

def insertar_empleado(nombre: str, apellido: str, correo: str, contraseña: str, genero: str, dni: int, rol_id: int):
    """Permite insertar una fila para la tabla Empleado"""
    cursor = conectarse_db()
    cursor.execute(f"""INSERT INTO Empleado (nombre, apellido, correo, contraseña, genero, dni, rol_id)
                                VALUES ('{nombre}', '{apellido}', '{correo}', '{contraseña}', '{genero}', {dni}, {rol_id});""")
    commitear(cursor)
