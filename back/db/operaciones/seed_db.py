from db.operaciones.insertar_db import insertar_usuario, insertar_profesor, insertar_actividad, insertar_mensualidad, insertar_permiso, insertar_rol
from pprint import pprint
import services.usuario_service as u_s
import datetime

def insertar_datos():
    respuesta = u_s.registrar_usuario_service(
        dni=123456789,  
        nombre='Juan',
        apellido='Pérez',
        contraseña='123',
        fecha_nac='2007-08-05',
        telefono='1234567890', 
        correo='juan.perez@example.com', 
        genero='M'
    )

    print("Respuesta del registro de usuario:")
    pprint(respuesta)
    print("\n")


    respuesta = u_s.registrar_usuario_service(
        dni=1234567891,
        nombre='San',
        apellido='Pérez',
        contraseña='123',
        fecha_nac= '2007-08-05',
        telefono='1234567890',
        correo='prueba10@example.com',
        genero='M'
    )

    print("Respuesta del registro de usuario:")
    pprint(respuesta)
    print("\n")

    respuesta = u_s.registrar_usuario_service(
        dni=12345678,  # DNI repetido
        nombre='Juan',
        apellido='Pérez',
        contraseña='123',
        fecha_nac=datetime.date(year=2006, month=10, day=5).strftime("%Y-%m-%d"),
        telefono='1234567890', 
        correo='prueba1@gmail.com', 
        genero='M'
    )

    print("Respuesta del registro de usuario:")
    pprint(respuesta)
    print("\n")

    insertar_roles()


def insertar_roles():
    insertar_rol("Administrador")
    insertar_rol("Recepcionista")
    insertar_rol("Profesor")