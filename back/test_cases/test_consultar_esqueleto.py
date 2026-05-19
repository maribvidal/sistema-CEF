from db.operaciones.consultar_db import obtener_rol_por_id
from db.operaciones.consultar_db import consultar_permiso_por_id
from db.operaciones.consultar_db import consultar_usuario_por_dni
from db.operaciones.consultar_db import consultar_usuario_por_correo
from db.operaciones.consultar_db import listar_clases
from db.operaciones.consultar_db import listar_usuarios
from db.operaciones.consultar_db import obtener_empleados
from db.operaciones.consultar_db import consultar_pagos_de_usuario
from db.operaciones.consultar_db import consultar_usuario_por_id

# TODO: Escribir mejor los tests, que expresen algo mas

def intentar_consultar_esqueleto():
    test_consultar_permiso_por_id()
    test_consultar_usuario_por_dni()
    test_consultar_usuario_por_correo()
    test_listar_clases()
    test_listar_usuarios()
    test_obtener_empleados()
    test_consultar_usuario_por_id()
    test_consultar_pagos_de_usuario()
    test_obtener_rol_por_id()

def test_consultar_permiso_por_id():
    print("Test consultar_permiso_por_id:")
    print("Test consultar_permiso_por_id:")
    print(consultar_permiso_por_id(1))  # Debería devolver el permiso con id 1
    print(consultar_permiso_por_id(999))  # Debería devolver una tupla vacía o None

def test_consultar_usuario_por_dni():
    print("Test consultar_usuario_por_dni:")
    print("Test consultar_usuario_por_dni:")
    print(consultar_usuario_por_dni(12345678))  # Debería devolver el usuario con ese DNI
    print(consultar_usuario_por_dni(99999999))  # Debería devolver una tupla vacía o None

def test_consultar_usuario_por_correo():
    print("Test consultar_usuario_por_correo:")
    print("Test consultar_usuario_por_correo:")
    print(consultar_usuario_por_correo('prueba1@gmail.com'))  # Debería devolver el usuario con ese correo
    print(consultar_usuario_por_correo('prueba999@gmail.com'))  # Debería devolver una tupla vacía o None

def test_listar_clases():
    print("Test listar_clases:")
    print("Test listar_clases:")
    print(listar_clases())  # Debería devolver una lista de tuplas con las clases

def test_listar_usuarios():
    print("Test listar_usuarios:")
    print("Test listar_usuarios:")
    print(listar_usuarios())  # Debería devolver una lista de tuplas con los usuarios

def test_obtener_empleados():
    print("Test obtener_empleados:")
    print("Test obtener_empleados:")
    print(obtener_empleados())  # Debería devolver una lista de tuplas con los empleados


def test_consultar_usuario_por_id():
    print("Test consultar_usuario_por_id:")
    print("Test consultar_usuario_por_id:")
    print(consultar_usuario_por_id(1))  # Debería devolver el usuario con id 1
    print(consultar_usuario_por_id(999))  # Debería devolver una tupla vacía o None


def test_consultar_pagos_de_usuario():
    print("Test consultar_pagos_de_usuario:")
    print("Test consultar_pagos_de_usuario:")
    print(consultar_pagos_de_usuario(1))  # Debería devolver una lista de tuplas con los pagos del usuario con id 1
    print(consultar_pagos_de_usuario(999))  # Debería devolver una lista vacía


def test_obtener_rol_por_id():
    print("Test obtener_rol_por_id:")
    print("Test obtener_rol_por_id:")
    print(obtener_rol_por_id(1))
    print(obtener_rol_por_id(999))
    assert(obtener_rol_por_id(1) is not None, "No se obtuvo el rol requerido")
