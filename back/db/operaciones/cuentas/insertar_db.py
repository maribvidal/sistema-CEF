from db.operaciones.conectar_db import conectarse_db
from db.operaciones.commitear_db import commitear

def insertar_cuenta(dni: int, nombre: str, apellido: str, contraseña: str, correo: str, genero: str) -> int:
    """Función que inserta una nueva cuenta en la base de datos."""
    cursor = conectarse_db()
    cursor.execute("INSERT INTO Cuenta (dni, nombre, apellido, contraseña, correo, genero) VALUES (?, ?, ?, ?, ?, ?)", (dni, nombre, apellido, contraseña, correo, genero))
    nuevo_id = cursor.lastrowid
    commitear(cursor)
    return nuevo_id
