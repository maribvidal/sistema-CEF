from db.operaciones import insertar_datos, listar_usuarios
from pprint import pprint

import datetime
import services.usuario_service as u_s


def intentar_insertar_datos(cursor):
    insertar_datos(cursor)
    insertar_actividades(cursor)
    insertar_profesores(cursor)
    insertar_clases(cursor)

    lista = listar_usuarios(cursor)
    print("Usuarios después de insertar datos:")
    pprint(lista)
    print("\n")

    print("Intentando insertar datos erróneos:")
    insertar_datos_erroneos()

def insertar_datos_erroneos():
    #checkeo de longitudes
    respuesta = u_s.registrar_usuario_service(
        dni=1,
        nombre='abcdefghijklmnopqrstuv',  # 21 caracteres, excede el límite de 20
        apellido='bcdefghijklmnopqrstuvwaasdasdasd',  # 32 caracteres, excede el límite de 30
        contraseña='12334567890123',  # 13 caracteres, excede el límite de 12
        fecha_nac=datetime.date(year=2005, month=10, day=5).strftime("%Y-%m-%d"),
        telefono='1234567890123451231231231231',  # 15 caracteres, dentro del límite
        correo='prueba1234567891234@example.com', # 31 caracteres, excede el límite de 30
        genero='M',
        rol=2
    )

    print("Respuesta del registro de usuario:")
    pprint(respuesta)
    print("\n")


    #checkeo de dni, correo repetidos
    respuesta = u_s.registrar_usuario_service(
        dni=12345678,  # DNI repetido
        nombre='Juan',
        apellido='Pérez',
        contraseña='123',
        fecha_nac=datetime.date(year=2006, month=10, day=5).strftime("%Y-%m-%d"),
        telefono='1234567890', 
        correo='prueba1@gmail.com', 
        genero='M',
        rol=1
    )

    print("Respuesta del registro de usuario:")
    pprint(respuesta)
    print("\n")

    # fecha inválida
    respuesta = u_s.registrar_usuario_service(
        dni=52345678,  # DNI repetido
        nombre='Juan',
        apellido='Pérez',
        contraseña='123',
        fecha_nac="elpepe",
        telefono='1234567890',
        correo='prueba10@gmail.com',
        genero='M',
        rol=3
    )

    print("Respuesta del registro de usuario:")
    pprint(respuesta)
    print("\n")

from db.operaciones import insertar_actividad, insertar_clase
def insertar_clases(cursor):
    insertar_clase("Yoga", 2, 1, cursor)
    insertar_clase("Pilates", 2, 2, cursor)

from db.operaciones import insertar_profesor
def insertar_profesores(cursor):
    insertar_profesor("Carlos", "García", "H", 5, cursor)
    insertar_profesor("Paez", "García", "H", 4, cursor)


# def insertar_actividad(nombre: str, precio_mensual: float):
from db.operaciones import insertar_actividad
def insertar_actividades(cursor):
    insertar_actividad("Yoga", 2000, cursor)
    insertar_actividad("Pilates", 2500, cursor)