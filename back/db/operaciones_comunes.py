from db.operaciones.cuentas.consultar_db import consultar_cuenta_por_id
from db.operaciones.cuentas.insertar_db import insertar_cuenta
from db.operaciones.usuarios.insertar_db import insertar_usuario

import sqlite3 as sqlite

# Estas operaciones van a manejar las excepciones que puedan
# surgir durante el proceso de manipulación de la BD, y van
# devolver True o False en base a si la operación se
# realizó con exito o no.

def crear_usuario(dni: int, nombre: str, apellido: str, contraseña: str, fecha_nac, correo: str, telefono: str, genero: str) -> bool:
    """Función de alto nivel para crear un nuevo usuario.
        Esta función se encarga de validar los datos de entrada,
        crear una entidad Cuenta, vincularla con la nueva
        entidad Usuario que se cree, y manejar las posibles
        excepciones que puedan surgir durante el proceso."""
    try:
        insertar_cuenta(dni, nombre, apellido, contraseña, correo, genero)
        insertar_usuario(dni, nombre, apellido, contraseña, fecha_nac, correo, telefono, genero)
        print(f"Usuario con dni {dni} cread exitosamente.")
        return True
    except sqlite.IntegrityError as e:
        print(f"Error de integridad: {e}")
        return False
    except Exception as e:
        print(f"Error desconocido: {e}")
        return False
