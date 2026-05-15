from db.operaciones.insertar_db import insertar_usuario
from db.operaciones.consultar_db import consultar_usuario_por_dni

# Los parametros los tomé en cuenta al ver los text-field del Registro.Vue del frontend, si se necesita agregar o quitar alguno, solo avisenme y lo modifico
def registrar_usuario(nombre: str, apellido: str, dni: int, correo: str, telefono: int, edad: int, contrasena: str) -> bool:
    # Verificar si el usuario ya existe realizando una constulta a la base de datos
    if consultar_usuario_por_dni(dni):
        print("El usuario ya está registrado")
        return False

    # Insertar el nuevo usuario
    insertar_usuario(dni, nombre, apellido, edad, contrasena, correo, telefono, "Otro")
    print("El usuario registrado exitosamente")
    return True


from db.operaciones.consultar_db import consultar_usuario_por_correo
# Los parametros los tomé en cuenta al ver los text-field del InicioSesionView.Vue del frontend, si se necesita agregar o quitar alguno, solo avisenme y lo modifico
# Voy a suponer que el text-field del usuario es el email, pero si es por usuario, entonces hay que implementar una función dentro de consultar_db.py que consulte por usuario, y no por correo, y luego importarla aquí para usarla en esta función    

# Función mejorada de iniciar sesión, para que devuelva los datos que le podrían servir al fronted para mostrar el nombre del usuario, o su correo, o lo que sea, y no solo un booleano
def iniciar_sesion(correo: str, contrasena: str):
    usuario = consultar_usuario_por_correo(correo)
    if not usuario:
        print("El usuario no está registrado")
        return False

    pos_contrasena = 5  # Viendo lo que devuelve la consulta, la contraseña está en la posición 5 de la tupla, pero esto puede cambiar dependiendo de cómo esté estructurada la base de datos, así que habría que verificarlo bien para no tener errores
    
    if usuario[pos_contrasena] == contrasena:  
        print("Inicio de sesión exitoso")
        return {
            "id": usuario[0],
            "dni": usuario[1],
            "nombre": usuario[2],
            "correo": usuario[6],
        }
    else:
        print("Contraseña incorrecta")
        return False

def cerrar_sesion():
    # Aca podes implementar la lógica para cerrar sesión.
    return

    
