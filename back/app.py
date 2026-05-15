from db import consultar_db as c_db
import sqlite3 as sqlite

conexion = sqlite.connect('database.db')
cursor = conexion.cursor()

tupla = c_db.consultar_usuario_por_correo('lozada@gmail.com')
print(tupla)