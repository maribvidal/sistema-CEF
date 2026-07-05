from db.operaciones.exception_handler import ejecutar_insertar
from utils.modulo_fechas import generar_fecha_hora_actual

def insertar_usuario(dni: int, nombre: str, apellido: str, contraseña: str, fecha_nac: str, correo: str, telefono: str, genero: str, rol: int, cursor):
    """Permite insertar una fila para la tabla Usuario"""
    query = f"""INSERT INTO Usuario (dni, nombre, apellido, contraseña, fecha_nac, correo, telefono, genero, rol_id)
                VALUES ({dni}, '{nombre}', '{apellido}', '{contraseña}', '{fecha_nac}', '{correo}', '{telefono}', '{genero}', {rol});"""
    return ejecutar_insertar(query, cursor)

def insertar_usuario_verificado(dni: int, nombre: str, apellido: str, contraseña: str, fecha_nac: str, correo: str, telefono: str, genero: str, rol: int, cursor):
    """Permite insertar una fila para la tabla Usuario"""
    query = f"""INSERT INTO Usuario (dni, nombre, apellido, contraseña, fecha_nac, correo, telefono, genero, rol_id, estado)
                VALUES ({dni}, '{nombre}', '{apellido}', '{contraseña}', '{fecha_nac}', '{correo}', '{telefono}', '{genero}', {rol}, {1});"""
    return ejecutar_insertar(query, cursor)

def insertar_usuario_lista_espera_abonados(id_lea: int, id_usuario: int, cursor):
    """Permite insertar a un usuario en una lista de espera de abonados."""
    fecha = generar_fecha_hora_actual()
    query = f"""INSERT INTO Usuario_Pertenece_Lista_Espera_Abonados (usuario_id, lea_id, fecha)
                                                        VALUES      ({id_usuario}, {id_lea}, '{fecha}');
    """
    return ejecutar_insertar(query, cursor)

def insertar_usuario_lista_espera_individual(id_lei: int, id_usuario: int, cursor):
    """Permite insertar a un usuario en una lista de espera individual."""
    fecha = generar_fecha_hora_actual()
    query = f"""INSERT INTO Usuario_Pertenece_Lista_Espera_Individual (usuario_id, lei_id, fecha)
                                                        VALUES      ({id_usuario}, {id_lei}, '{fecha}');
        """
    return ejecutar_insertar(query, cursor)
