from db.operaciones import obtener_rol_por_id, consultar_permiso_por_id, consultar_usuario_por_dni, consultar_usuario_por_correo ,listar_clases ,listar_usuarios, consultar_pagos_de_usuario, consultar_usuario_por_id

# TODO: Escribir mejor los tests, que expresen algo mas

def intentar_consultar_esqueleto(cursor):
    test_consultar_permiso_por_id(cursor)
    test_consultar_usuario_por_dni(cursor)
    test_consultar_usuario_por_correo(cursor)
    test_listar_clases(cursor)
    test_listar_usuarios(cursor)
    test_consultar_usuario_por_id(cursor)
    test_consultar_pagos_de_usuario(cursor)
    test_obtener_rol_por_id(cursor)
    cursor.connection.close()

def test_consultar_permiso_por_id(cursor):
    print("---------------TEST CONSULTAR PERMISO POR ID---------------")
    print("Primer test (debe devolver el permiso):")
    res = procesar_consulta(consultar_permiso_por_id(1, cursor))
    if res is not None:
        print(res[0])

    print("Segundo test (debe devolver una tupla vacía o None):")
    res = procesar_consulta(consultar_permiso_por_id(999, cursor))
    print(res)



def test_consultar_usuario_por_dni(cursor):
    print("---------------TEST CONSULTAR USUARIO POR DNI---------------")
    print("Test consultar_usuario_por_dni (deberia devolver el usuario con DNI 123456789):") 
    res = procesar_consulta(consultar_usuario_por_dni(12345678, cursor))
    if res is not None:
        print(res[1])

    print("Test consultar_usuario_por_dni (deberia devolver una tupla vacía o None):")
    res = procesar_consulta(consultar_usuario_por_dni(99999999, cursor))
    print(res)
    print("\n")

def test_consultar_usuario_por_correo(cursor):
    print("---------------TEST CONSULTAR USUARIO POR CORREO---------------")
    print("Test consultar_usuario_por_correo (deberia devolver el usuario con correo prueba1@gmail.com):")
    res = procesar_consulta(consultar_usuario_por_correo('juan.perez@example.com', cursor))
    if res is not None:
        print(res[0])

    print("Test consultar_usuario_por_correo (deberia devolver una tupla vacía o None):")
    res = procesar_consulta(consultar_usuario_por_correo('correo_inexistente@tumama.com', cursor))
    print(res)
    print("\n")


def test_listar_clases(cursor):
    print("---------------TEST LISTAR CLASES---------------")
    res = procesar_consulta(listar_clases(cursor))
    print(res)
    print("\n")


def test_listar_usuarios(cursor):
    print("---------------TEST LISTAR USUARIOS---------------")
    res = procesar_consulta(listar_usuarios(cursor))
    print(res)
    print("\n")

def test_consultar_usuario_por_id(cursor):
    print("---------------TEST CONSULTAR USUARIO POR ID---------------")
    print("Test consultar_usuario_por_id (deberia devolver el usuario con id 1):") 
    res = procesar_consulta(consultar_usuario_por_id(1, cursor))
    if res is not None:
        print(res[1])

    print("Test consultar_usuario_por_id (deberia devolver una tupla vacía o None):")
    res = procesar_consulta(consultar_usuario_por_id(999, cursor))
    print(res)
    print("\n")


def test_consultar_pagos_de_usuario(cursor):
    print("---------------TEST CONSULTAR PAGOS DE USUARIO---------------")
    print("Test consultar_pagos_de_usuario (deberia devolver una lista de tuplas con los pagos del usuario con id 1 o vacío, por ahora seguramente dé vacío):") 
    res = procesar_consulta(consultar_pagos_de_usuario(1, cursor))
    print(res)
    print("Test consultar_pagos_de_usuario (deberia devolver una lista vacía):")
    res = procesar_consulta(consultar_pagos_de_usuario(999, cursor))
    print(res)
    print("\n")


def test_obtener_rol_por_id(cursor):
    print("---------------TEST OBTENER ROL POR ID---------------")
    print("Test obtener_rol_por_id (deberia devolver el rol con id 1):") 
    res = procesar_consulta(obtener_rol_por_id(1, cursor))
    if res is not None:
        print(res[1])

    print("Test obtener_rol_por_id (deberia devolver una tupla vacía o None):")
    res = procesar_consulta(obtener_rol_por_id(999, cursor))
    print(res)
    print("\n")


def procesar_consulta(consulta: dict) -> tuple | None:
    if consulta['status'] == 'success' and consulta['data'] is not None:
        print("Consulta exitosa: " )
        return consulta["data"]
    elif consulta['status'] == 'success' and consulta['data'] is None:
        print("Consulta exitosa pero no se encontró ningún resultado:" )
        return None
    else:
        print("Consulta fallida...")
        return None


