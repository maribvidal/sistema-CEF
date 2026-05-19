from db.operaciones.construir_db import reconstruir_db
from db.operaciones.conectar_db import conectarse_db
from db.operaciones.insertar_datos_prueba import insertar_datos
from db.operaciones.consultar_db import listar_usuarios

import datetime

reconstruir_db()
cursor = conectarse_db()

insertar_datos()

#tupla1 = c_db.consultar_usuario_por_correo('lozada@gmail.com')
#tupla2 = c_db.consultar_usuario_por_correo('juan.perez@example.com')

#print(tupla1)
#print(tupla2)

lista = listar_usuarios()
print(lista)

import services.usuario_service as u_s

#checkeo de longitudes
respuesta = u_s.registrar_usuario_service(
    dni=1,
    nombre='abcdefghijklmnopqrstuv',  # 21 caracteres, excede el límite de 20
    apellido='bcdefghijklmnopqrstuvwaasdasdasd',  # 32 caracteres, excede el límite de 30
    contraseña='12334567890123',  # 13 caracteres, excede el límite de 12
    fecha_nac=datetime.date(day=10,month=10,year=2004),
    telefono='1234567890123451231231231231',  # 15 caracteres, dentro del límite
    correo='prueba1234567891234@example.com', # 31 caracteres, excede el límite de 30
    genero='M',
)

print(respuesta)

#checkeo de dni, correo repetidos, fecha inválida y edad minima
respuesta = u_s.registrar_usuario_service(
    dni=12345678,  # DNI repetido
    nombre='Juan',
    apellido='Pérez',
    contraseña='123',
    fecha_nac="pepe",
    telefono='1234567890', 
    correo='prueba1@gmail.com', 
    genero='M'
)

print(respuesta)

respuesta = u_s.registrar_usuario_service(
    dni=123456789,  
    nombre='Juan',
    apellido='Pérez',
    contraseña='123',
    fecha_nac=datetime.date(day=10,month=10,year=2008),
    telefono='1234567890', 
    correo='juan.perez@example.com', # Correo repetido 
    genero='M'
)

print(respuesta)

respuesta = u_s.registrar_usuario_service(
    dni=123456789,  
    nombre='Juan',
    apellido='Pérez',
    contraseña='123',
    fecha_nac=datetime.date(day=10,month=10,year=2020),
    telefono='1234567890', 
    correo='prueba@example.com',  
    genero='M'
)

print(respuesta)


respuesta = u_s.registrar_usuario_service(
    dni=1234567891,  
    nombre='Juan',
    apellido='Pérez',
    contraseña='123',
    fecha_nac=datetime.date(day=5,month=10,year=2008),
    telefono='1234567890', 
    correo='prueba@example.com',  
    genero='M'
)

print(respuesta)

lista = listar_usuarios()
print(lista)

cursor.connection.close()

from flask import Flask
from routes import *

app = Flask(__name__)

# hay que ver si se puede modularizar esto para no agregar de a uno
app.register_blueprint(usuario_bp)
app.register_blueprint(autenticacion_bp)
app.register_blueprint(clases_bp)
app.register_blueprint(empleados_bp)

if __name__ == "__main__":
    app.run(debug=True)
