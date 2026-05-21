from pprint import pprint
import services.autenticacion_service as a_s

def intentar_login_service(cursor):
    # --- PRUEBAS DE LOGUEO ---
    print("\n--- TESTEO DE LOGIN ---")

    # 1. Intentar loguear un usuario que SÍ existe (Juan Pérez, que viene en los datos de prueba)
    correo = 'juan.perez@example.com'
    contraseña = '123'
    login_exitoso = a_s.login_service(correo, contraseña)
    # 2. Intentar loguear con contraseña incorrecta
    contraseña = 'clave_falsa'
    login_clave_mal = a_s.login_service(correo, contraseña)
    # 3. Intentar loguear un correo que no existe
    correo = 'no_existo@gimnasio.com'
    contraseña = '123'
    login_fantasma = a_s.login_service(correo, contraseña)

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
