from decoradores.decoradores_operaciones import conectar_y_commitear
import sqlite3 as sqlite

### TODO:
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

## FUNCIONES QUE INSERTAN FILAS EN LAS TABLAS DE LA BD

@conectar_y_commitear
def insertar_actividad(cursor: sqlite.Cursor, nombre: str, precio_mensual: float):
    """Permite insertar una fila para la tabla Actividad"""
    cursor.execute(f"""INSERT INTO Actividad (nombre, precio_mensual)
                                VALUES ('{nombre}', {precio_mensual});""")

@conectar_y_commitear
def insertar_mensualidad(cursor: sqlite.Cursor, fecha_ini, fecha_fin, usuario_id: int):
    """Permite insertar una fila para la tabla Mensualidad"""
    cursor.execute(f"""INSERT INTO Mensualidad (fecha_ini, fecha_fin, usuario_id)
                                VALUES ('{fecha_ini}', '{fecha_fin}', {usuario_id});""")

@conectar_y_commitear
def insertar_permiso(cursor: sqlite.Cursor, nombre: str):
    """Permite insertar una fila para la tabla Permiso"""
    cursor.execute(f"""INSERT INTO Permiso (nombre)
                                VALUES ('{nombre}');""")

@conectar_y_commitear
def insertar_profesor(cursor: sqlite.Cursor, nombre: str, apellido: str, genero: str, dni: int):
    """Permite insertar una fila para la tabla Profesor"""
    cursor.execute(f"""INSERT INTO Profesor (nombre, apellido, genero, dni)
                                VALUES('{nombre}', '{apellido}', '{genero}', '{dni}');""")

@conectar_y_commitear
def insertar_rol(cursor: sqlite.Cursor, nombre: str):
    """Permite insertar una fila para la tabla Rol"""
    cursor.execute(f"""INSERT INTO Rol (nombre) 
                                VALUES ('{nombre}');""")

@conectar_y_commitear
def insertar_usuario(cursor: sqlite.Cursor, dni: int, nombre: str, apellido: str, contraseña: str, correo: str, telefono: int, genero: str):
    """Permite insertar una fila para la tabla Usuario"""
    cursor.execute(f"""INSERT INTO Usuario (dni, nombre, apellido, contraseña, correo, telefono, genero)
                                VALUES({dni}, '{nombre}', '{apellido}', '{contraseña}', '{correo}', '{telefono}', '{genero}');""")
