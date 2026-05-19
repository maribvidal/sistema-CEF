from db.operaciones import obtener_rol_por_id, consultar_permiso_por_id, consultar_usuario_por_dni, consultar_usuario_por_correo ,listar_clases ,listar_usuarios, obtener_empleados, consultar_pagos_de_usuario, consultar_usuario_por_id

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
    print("---------------TEST CONSULTAR PERMISO POR ID---------------")
    print("Primer test (debe devolver el permiso):")
    print(consultar_permiso_por_id(1))
    print("Segundo test (debe devolver tupla vacía o None):")
    consultar_permiso_por_id(999)
    print("\n")

def test_consultar_usuario_por_dni():
    print("---------------TEST CONSULTAR USUARIO POR DNI---------------")
    usuario = consultar_usuario_por_dni(123456789)
    if usuario:
        print("Test consultar_usuario_por_dni (deberia devolver el usuario con DNI 123456789):" + str(usuario[1]))
    else:
        print("Test consultar_usuario_por_dni (deberia devolver el usuario con DNI 123456789): No se encontró el usuario")
    print("\n")

def test_consultar_usuario_por_correo():
    print("---------------TEST CONSULTAR USUARIO POR CORREO---------------")
    usuario = consultar_usuario_por_correo('prueba1@gmail.com')
    if usuario:
        print("Test consultar_usuario_por_correo (deberia devolver el usuario con correo prueba1@gmail.com):" + str(usuario[2]))
    else:
        print("Test consultar_usuario_por_correo (deberia devolver el usuario con correo prueba1@gmail.com): No se encontró el usuario")
    print("\n")

def test_listar_clases():
    print("---------------TEST LISTAR CLASES---------------")
    clases = listar_clases()
    if not clases:
        print("No hay clases.")
    else:
        for c in clases:
            print(c[1])  # Imprimir el nombre de la actividad
    print("\n")


def test_listar_usuarios():
    print("---------------TEST LISTAR USUARIOS---------------")
    usuarios = listar_usuarios()
    print("Test listar_usuarios (listando solo nombres de usuarios):")
    if not usuarios:
        print("No hay usuarios.")
    else:
        for u in usuarios:
            nombre = u[2] if len(u) > 2 else str(u)
            print(nombre)
    print("\n")

def test_obtener_empleados():
    print("---------------TEST OBTENER EMPLEADOS---------------")
    print("Test obtener_empleados (deberia devolver una lista de tuplas con los empleados o vacío):" + str(obtener_empleados()))
    print("\n")

def test_consultar_usuario_por_id():
    print("---------------TEST CONSULTAR USUARIO POR ID---------------")
    print("Test consultar_usuario_por_id (deberia devolver el usuario con id 1):" + str(consultar_usuario_por_id(1)[2]))
    print("Test consultar_usuario_por_id (deberia devolver una tupla vacía o None):" + str(consultar_usuario_por_id(999)))
    print("\n")


def test_consultar_pagos_de_usuario():
    print("---------------TEST CONSULTAR PAGOS DE USUARIO---------------")
    print("Test consultar_pagos_de_usuario (deberia devolver una lista de tuplas con los pagos del usuario con id 1 o vacío, por ahora seguramente dé vacío):" + str(consultar_pagos_de_usuario(1)))
    print("Test consultar_pagos_de_usuario (deberia devolver una lista vacía):" + str(consultar_pagos_de_usuario(999)))
    print("\n")


def test_obtener_rol_por_id():
    print("---------------TEST OBTENER ROL POR ID---------------")
    print("Test obtener_rol_por_id (deberia devolver el rol con id 1):" + str(obtener_rol_por_id(1)[1]))
    print("Test obtener_rol_por_id (deberia devolver una tupla vacía o None):" + str(obtener_rol_por_id(999)))
    print("\n")
