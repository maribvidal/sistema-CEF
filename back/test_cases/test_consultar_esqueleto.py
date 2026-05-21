from db.operaciones import obtener_rol_por_id, consultar_permiso_por_id, consultar_usuario_por_dni, consultar_usuario_por_correo ,listar_clases ,listar_usuarios, obtener_empleados, consultar_pagos_de_usuario, consultar_usuario_por_id

# TODO: Escribir mejor los tests, que expresen algo mas

def intentar_consultar_esqueleto(cursor):
    test_consultar_permiso_por_id(cursor)
    test_consultar_usuario_por_dni(cursor)
    test_consultar_usuario_por_correo(cursor)
    test_listar_clases(cursor)
    test_listar_usuarios(cursor)
    test_obtener_empleados(cursor)
    test_consultar_usuario_por_id(cursor)
    test_consultar_pagos_de_usuario(cursor)
    test_obtener_rol_por_id(cursor)

def test_consultar_permiso_por_id(cursor):
    print("---------------TEST CONSULTAR PERMISO POR ID---------------")
    print("Primer test (debe devolver el permiso):")
    print(consultar_permiso_por_id(1,cursor))
    print("Segundo test (debe devolver tupla vacía o None):")
    consultar_permiso_por_id(999,cursor)
    print("\n")

def test_consultar_usuario_por_dni(cursor):
    print("---------------TEST CONSULTAR USUARIO POR DNI---------------")
    usuario = consultar_usuario_por_dni(123456789, cursor)
    if usuario['status'] == 'success' and usuario['data'] is not None:
        print("Test consultar_usuario_por_dni (deberia devolver el usuario con DNI 123456789):" + str(usuario['data']))
    elif usuario['status'] == 'success':
        print("Test consultar_usuario_por_dni (deberia devolver el usuario con DNI 123456789): No se encontró el usuario")
    else:
        print("Test consultar_usuario_por_dni (deberia devolver el usuario con DNI 123456789): Error al ejecutar la consulta: " + str(usuario['message']))
    print("\n")

def test_consultar_usuario_por_correo(cursor):
    print("---------------TEST CONSULTAR USUARIO POR CORREO---------------")
    usuario = consultar_usuario_por_correo('prueba1@gmail.com', cursor)
    if usuario['status'] == 'success' and usuario['data'] is not None:
        print("Test consultar_usuario_por_correo (deberia devolver el usuario con correo prueba1@gmail.com):" + str(usuario['data']))
    elif usuario['status'] == 'success':
        print("Test consultar_usuario_por_correo (deberia devolver el usuario con correo prueba1@gmail.com): No se encontró el usuario")
    else:
        print("Test consultar_usuario_por_correo (deberia devolver el usuario con correo prueba1@gmail.com): Error al ejecutar la consulta: " + str(usuario['message']))
    print("\n")

def test_listar_clases(cursor):
    print("---------------TEST LISTAR CLASES---------------")
    clases = listar_clases(cursor)
    if not clases:
        print("No hay clases.")
    else:
        for c in clases:
            print(c[1])  # Imprimir el nombre de la actividad
    print("\n")


def test_listar_usuarios(cursor):
    print("---------------TEST LISTAR USUARIOS---------------")
    usuarios = listar_usuarios(cursor)
    print("Test listar_usuarios (listando solo nombres de usuarios):")
    if not usuarios:
        print("No hay usuarios.")
    else:
        for u in usuarios:
            nombre = u[2] if len(u) > 2 else str(u)
            print(nombre)
    print("\n")

def test_obtener_empleados(cursor):
    print("---------------TEST OBTENER EMPLEADOS---------------")
    print("Test obtener_empleados (deberia devolver una lista de tuplas con los empleados o vacío):" + str(obtener_empleados(cursor)))
    print("\n")

def test_consultar_usuario_por_id(cursor):
    print("---------------TEST CONSULTAR USUARIO POR ID---------------")
    usuario = consultar_usuario_por_id(1, cursor)
    if usuario['status'] == 'success' and usuario['data'] is not None:
        print("Test consultar_usuario_por_id (deberia devolver el usuario con id 1):" + str(usuario['data'][2]))
    else:
        print("Test consultar_usuario_por_id (deberia devolver una tupla vacía o None):" + str(usuario['data']))
    print("\n")


def test_consultar_pagos_de_usuario(cursor):
    print("---------------TEST CONSULTAR PAGOS DE USUARIO---------------")
    print("Test consultar_pagos_de_usuario (deberia devolver una lista de tuplas con los pagos del usuario con id 1 o vacío, por ahora seguramente dé vacío):" + str(consultar_pagos_de_usuario(1, cursor)))
    print("Test consultar_pagos_de_usuario (deberia devolver una lista vacía):" + str(consultar_pagos_de_usuario(999, cursor)))
    print("\n")


def test_obtener_rol_por_id(cursor):
    print("---------------TEST OBTENER ROL POR ID---------------")
    res = obtener_rol_por_id(1, cursor)
    if res['status'] == 'success' and res['data'] is not None:
        print("Test obtener_rol_por_id (deberia devolver el rol con id 1):" + str(res['data'][1]))
    res = obtener_rol_por_id(999, cursor)
    if res['status'] == 'success' and res['data'] is not None:
        print("Test obtener_rol_por_id (deberia devolver una tupla vacía o None):" + str(res['data']))
    print("\n")
