import sqlite3 as sqlite

# CONSTANTES
from db import NOM_DB

### - Hacer un wrapper para que cualquiera de estas funciones
###   no haga que se detenga el main si es que reciben una
###   excepción. Implementar un exception handler.
### - ¿Cómo guardamos las contraseñas?
### - ¿Qué tipo de dato usamos con las fechas? Definir para estandarizar.
### - ¿Debería crear un tipo de dato para solucionar el bad smell de
###   Long Parameter List?
### - ¿Debería hacer una validación previa para los datos antes
###   de enviarlos a la BD?
### - ¿Cómo reacciono ante los errores de parte del motor de la BD?
### - ¿Cómo devuelvo los errores de Foreign Keys?

def conectarse_db() -> sqlite.Cursor:
    """Crea una conexión a la BD y devuelve un objeto Cursor"""
    conexion = sqlite.connect(NOM_DB)
    cursor = conexion.cursor()
    # Habilitar el control de Foreign Keys
    cursor.execute("PRAGMA foreign_keys = ON;")
    return cursor

def commitear(cursor: sqlite.Cursor):
    """Recibe un Cursor y con él hace commit y cierra la conexión con la BD"""
    cursor.connection.commit()
    cursor.connection.close()

## FUNCIONES QUE INSERTAN FILAS EN LAS TABLAS DE LA BD

def insertar_actividad(nombre: str, precio_mensual: float):
    """Permite insertar una fila para la tabla Actividad"""
    cursor = conectarse_db()
    cursor.execute(f"""INSERT INTO Actividad (nombre, precio_mensual)
                                VALUES ('{nombre}', {precio_mensual});""")
    commitear(cursor)

def insertar_mensualidad(fecha_ini, fecha_fin, usuario_id: int):
    """Permite insertar una fila para la tabla Mensualidad"""
    cursor = conectarse_db()
    cursor.execute(f"""INSERT INTO Mensualidad (fecha_ini, fecha_fin, usuario_id)
                                VALUES ('{fecha_ini}', '{fecha_fin}', {usuario_id});""")
    commitear(cursor)

def insertar_permiso(nombre: str):
    """Permite insertar una fila para la tabla Permiso"""
    cursor = conectarse_db()
    cursor.execute(f"""INSERT INTO Permiso (nombre)
                                VALUES ('{nombre}');""")
    commitear(cursor)

def insertar_profesor(nombre: str, apellido: str, genero: str, dni: int):
    """Permite insertar una fila para la tabla Profesor"""
    cursor = conectarse_db()
    cursor.execute(f"""INSERT INTO Profesor (nombre, apellido, genero, dni)
                                VALUES('{nombre}', '{apellido}', '{genero}', '{dni}');""")
    commitear(cursor)

def insertar_rol(nombre: str):
    """Permite insertar una fila para la tabla Rol"""
    cursor = conectarse_db()
    cursor.execute(f"""INSERT INTO Rol (nombre) 
                                VALUES ('{nombre}');""")
    commitear(cursor)

def insertar_usuario(dni: int, nombre: str, apellido: str, edad: int, contraseña: str, correo: str, telefono: int, genero: str):
    """Permite insertar una fila para la tabla Usuario"""
    cursor = conectarse_db()
    cursor.execute(f"""INSERT INTO Usuario (dni, nombre, apellido, edad, contraseña, correo, telefono, genero)
                                VALUES({dni}, '{nombre}', '{apellido}', {edad}, '{contraseña}', '{correo}', '{telefono}', '{genero}');""")
    commitear(cursor)