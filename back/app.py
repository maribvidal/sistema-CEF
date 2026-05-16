from db.operaciones import construir_db
from db.operaciones import consultar_db as c_db
import sqlite3 as sqlite
from db.operaciones import insertar_db

construir_db.construir_db()
conexion = sqlite.connect('database.db')
cursor = conexion.cursor()


# def insertar_usuario(dni: int, nombre: str, apellido: str, edad: int, contraseña: str, correo: str, telefono: int, genero: str):
insertar_db.insertar_usuario(12345678, 'Federico', 'Lozada', 22, 'contra123', 'lozada@gmail.com', 123456789, 'Masculino')

# Esto es para ver en qué posición se encuentra la contraseña, para luego usar esa posición en la función de iniciar sesión, para comparar la contraseña que me pasan por parámetro con la que tengo en la base de datos
tupla = c_db.consultar_usuario_por_correo('lozada@gmail.com')

print(tupla)