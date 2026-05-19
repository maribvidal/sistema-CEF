from db.operaciones.construir_db import reconstruir_db
from db.operaciones.conectar_db import conectarse_db
from db.operaciones.insertar_datos_prueba import insertar_datos
from db.operaciones.consultar_db import listar_usuarios
import services.usuario_service as u_s
import services.autenticacion_service as a_s 
from pprint import pprint # esto para ver el print mas bonito

reconstruir_db()
cursor = conectarse_db()

insertar_datos()

#tupla1 = c_db.consultar_usuario_por_correo('lozada@gmail.com')
#tupla2 = c_db.consultar_usuario_por_correo('juan.perez@example.com')

#print(tupla1)
#print(tupla2)

lista = listar_usuarios()
pprint(lista)

#checkeo de longitudes
respuesta = u_s.registrar_usuario_service(
    dni=1,
    nombre='abcdefghijklmnopqrstuv',  # 21 caracteres, excede el límite de 20
    apellido='bcdefghijklmnopqrstuvwaasdasdasd',  # 32 caracteres, excede el límite de 30
    contraseña='12334567890123',  # 13 caracteres, excede el límite de 12
    telefono='1234567890123451231231231231',  # 15 caracteres, dentro del límite
    correo='prueba1234567891234@example.com', # 31 caracteres, excede el límite de 30
    genero='M',
    edad=25
)

pprint(respuesta)

#checkeo de dni, correo repetidos y edad minima
respuesta = u_s.registrar_usuario_service(
    dni=12345678,  # DNI repetido
    nombre='Juan',
    apellido='Pérez',
    contraseña='123',
    telefono='1234567890', 
    correo='prueba1@gmail.com', 
    genero='M',
    edad=25
)

pprint(respuesta)

respuesta = u_s.registrar_usuario_service(
    dni=123456789,  
    nombre='Juan',
    apellido='Pérez',
    contraseña='123',
    telefono='1234567890', 
    correo='juan.perez@example.com', # Correo repetido 
    genero='M',
    edad=25
)

pprint(respuesta)

respuesta = u_s.registrar_usuario_service(
    dni=123456789,  
    nombre='Juan',
    apellido='Pérez',
    contraseña='123',
    telefono='1234567890', 
    correo='prueba@example.com',  
    genero='M',
    edad=5 # edad menor
)

pprint(respuesta)


respuesta = u_s.registrar_usuario_service(
    dni=1234567891,  
    nombre='Juan',
    apellido='Pérez',
    contraseña='123',
    telefono='1234567890', 
    correo='prueba@example.com',  
    genero='M',
    edad=25
)

pprint(respuesta)

lista = listar_usuarios()
pprint(lista)

cursor.connection.close()

from flask import Flask
from flask_cors import CORS
from routes import *

app = Flask(__name__)
CORS(app)

# hay que ver si se puede modularizar esto para no agregar de a uno
app.register_blueprint(usuario_bp)
app.register_blueprint(autenticacion_bp)
app.register_blueprint(clases_bp)
app.register_blueprint(empleados_bp)

# --- PRUEBAS DE LOGUEO ---
print("\n--- TESTEO DE LOGIN ---")

# 1. Intentar loguear un usuario que SÍ existe (Juan Pérez, que viene en los datos de prueba)
login_exitoso = a_s.login_service(correo='juan.perez@example.com', contraseña='123')
# 2. Intentar loguear con contraseña incorrecta
login_clave_mal = a_s.login_service(correo='juan.perez@example.com', contraseña='clave_falsa')
# 3. Intentar loguear un correo que no existe
login_fantasma = a_s.login_service(correo='no_existo@gimnasio.com', contraseña='123')

# --- PRUEBAS DE LOGUEO ---
print("\n--- TESTEO DE LOGIN ---")

# 1. Intentar loguear un usuario que SÍ existe
print("Login Juan (Debería ser 200):")
pprint(login_exitoso)

# 2. Intentar loguear con contraseña incorrecta
print("\nLogin clave incorrecta (Debería ser 400):")
pprint(login_clave_mal)

# 3. Intentar loguear un correo que no existe
print("\nLogin usuario inexistente (Debería ser 404):")
pprint(login_fantasma)




# --- TEST CASES CONSULTAR BASE DE DATOS ---
import test_cases.test_cases_consulta_db as c_db
c_db.consultar_esqueleto()



if __name__ == "__main__":
    app.run(debug=True)
