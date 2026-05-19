from db.operaciones.seed_db import insertar_datos
from db.operaciones.consultar_db import listar_usuarios
from pprint import pprint

import datetime
import services.usuario_service as u_s

def intentar_insertar_datos():
    insertar_datos()

    lista = listar_usuarios()
    pprint(lista)

    #checkeo de longitudes
    respuesta = u_s.registrar_usuario_service(
        dni=1,
        nombre='abcdefghijklmnopqrstuv',  # 21 caracteres, excede el límite de 20
        apellido='bcdefghijklmnopqrstuvwaasdasdasd',  # 32 caracteres, excede el límite de 30
        contraseña='12334567890123',  # 13 caracteres, excede el límite de 12
        fecha_nac=datetime.date(year=2005, month=10, day=5),
        telefono='1234567890123451231231231231',  # 15 caracteres, dentro del límite
        correo='prueba1234567891234@example.com', # 31 caracteres, excede el límite de 30
        genero='M'
    )

    pprint(respuesta)

    #checkeo de dni, correo repetidos
    respuesta = u_s.registrar_usuario_service(
        dni=12345678,  # DNI repetido
        nombre='Juan',
        apellido='Pérez',
        contraseña='123',
        fecha_nac=datetime.date(year=2006, month=10, day=5),
        telefono='1234567890', 
        correo='prueba1@gmail.com', 
        genero='M'
    )

    pprint(respuesta)

    # fecha inválida
    respuesta = u_s.registrar_usuario_service(
        dni=52345678,  # DNI repetido
        nombre='Juan',
        apellido='Pérez',
        contraseña='123',
        fecha_nac="elpepe",
        telefono='1234567890',
        correo='prueba10@gmail.com',
        genero='M'
    )

    pprint(respuesta)

    respuesta = u_s.registrar_usuario_service(
        dni=123456789,  
        nombre='Juan',
        apellido='Pérez',
        contraseña='123',
        fecha_nac='2007-08-05',
        telefono='1234567890', 
        correo='juan.perez@example.com', # Correo repetido 
        genero='M'
    )

    pprint(respuesta)

    respuesta = u_s.registrar_usuario_service(
        dni=123456789,
        nombre='Juan',
        apellido='Pérez',
        contraseña='123',
        fecha_nac='2007-08-05',
        telefono='1234567890',
        correo='prueba@example.com',
        genero='M'
    )

    pprint(respuesta)

    respuesta = u_s.registrar_usuario_service(
        dni=1234567891,
        nombre='Juan',
        apellido='Pérez',
        contraseña='123',
        fecha_nac=datetime.date(year=2005, month=10, day=5),
        telefono='1234567890',
        correo='prueba@example.com',
        genero='M'
    )

    pprint(respuesta)

    lista = listar_usuarios()
    pprint(lista)
