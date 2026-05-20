from db.operaciones.exception_handler import ejecutar_insertar 
from db.operaciones.cuentas import insertar_cuenta

def insertar_usuario(dni: int, nombre: str, apellido: str, contraseña: str, fecha_nac: str, correo: str, telefono: str, genero: str):
    """Permite insertar una fila para la tabla Usuario"""
    insertar_cuenta(dni, nombre, apellido, contraseña, correo, genero)
    return ejecutar_insertar(f"""
            INSERT INTO Usuario (dni, fecha_nac, telefono)
            VALUES({dni}, '{fecha_nac}', '{telefono}');
        """)
