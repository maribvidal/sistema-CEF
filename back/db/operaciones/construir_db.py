import sqlite3 as sqlite
import os

# CONSTANTES

# LONG_NOM = 20
# LONG_APE = 30
# LONG_CORREO = 30
# LONG_CONTRA = 12
# LONG_TEL = 15
# NOM_DB = "database.db"

### TO-DO:
### - ¿Cambiamos las opciones del ON DELETE y del ON UPDATE?
from db import LONG_TEL, NOM_DB, LONG_NOM, LONG_APE, LONG_CORREO, LONG_CONTRA, LONG_TEL

def reconstruir_db():
    """Destruye la BD y luego la vuelve a construir"""
    try:
        os.remove(os.getcwd() + '/' + NOM_DB)
    except FileNotFoundError:
        pass
    construir_db()

def construir_db():
    """Construye la BD si no existía antes"""
    conexion = sqlite.connect(NOM_DB)

    # Y con este podemos ejecutar y obtener resultados de
    # sentencias SQL de la BD
    cursor = conexion.cursor()

    # Habilitar Foreign Keys
    cursor.execute("PRAGMA foreign_keys = ON")

    # Ejecutar funciones que crean las tablas
    construir_tablas(cursor)

    # Prueba de que la BD se creó exitosamente 
    res = cursor.execute("SELECT name FROM sqlite_master")
    print(res.fetchall())

    # Cerrar la conexión
    conexion.close()

def construir_tablas(cursor: sqlite.Cursor):
    """Construye todas las tablas de la BD"""
    # Construir tablas para las entidades
    construir_tabla_permiso(cursor)
    construir_tabla_rol(cursor)
    construir_tabla_actividad(cursor)
    construir_tabla_profesor(cursor)
    construir_tabla_sala(cursor)
    construir_tabla_descuento(cursor)
    construir_tabla_usuario(cursor)
    construir_tabla_empleado(cursor) # necesita Rol
    construir_tabla_clase(cursor)    # necesita Actividad y Profesor
    construir_tabla_pago(cursor)     # necesita Usuario
    construir_tabla_mensualidad(cursor) # necesita Usuario

    # Construir tablas para las relaciones
    construir_tabla_administrador(cursor)  # necesita Empleado
    construir_tabla_recepcionista(cursor)  # necesita Empleado
    construir_tabla_rol_tener_permiso(cursor)
    construir_tabla_clase_ocurrir_sala(cursor)
    construir_tabla_usuario_tener_descuento(cursor)
    construir_tabla_usuario_inscribir_clase(cursor)
    construir_tabla_usuario_cancelar_clase(cursor)
    construir_tabla_pago_pagar_clase(cursor)
    construir_tabla_pago_pagar_mensualidad(cursor)
    construir_tabla_clase_tener_mensualidad(cursor)

## FUNCIONES QUE CREAN TABLAS
# En este apartado aparecen todas las funciones que crean
# alguna tabla de la BD.

def construir_tabla_administrador(cursor: sqlite.Cursor):
    """Construye la tabla Administrador"""
    cursor.execute("""CREATE TABLE IF NOT EXISTS Administrador (
                            id          INTEGER PRIMARY KEY,
                            dni         INTEGER UNIQUE NOT NULL,
                            FOREIGN KEY (dni) REFERENCES Empleado(dni)
                                        ON UPDATE CASCADE
                                        ON DELETE SET NULL
                        )""")

def construir_tabla_empleado(cursor: sqlite.Cursor):
    """Construye la tabla Empleado"""
    cursor.execute(f"""CREATE TABLE IF NOT EXISTS Empleado (
                            id          INTEGER PRIMARY KEY,
                            nombre      VARCHAR({LONG_NOM}),
                            apellido    VARCHAR({LONG_APE}),
                            correo      VARCHAR({LONG_CORREO}),
                            contraseña  VARCHAR({LONG_CONTRA}),
                            genero      CHAR(1) CHECK(length(genero) <= 1),
                            dni         INTEGER UNIQUE NOT NULL,
                            rol_id      INTEGER NOT NULL,
                            FOREIGN KEY (rol_id) REFERENCES Rol(id)
                                        ON UPDATE CASCADE
                                        ON DELETE SET NULL
                        )""")

def construir_tabla_permiso(cursor: sqlite.Cursor):
    """Construye la tabla Permiso"""
    cursor.execute(f"""CREATE TABLE IF NOT EXISTS Permiso (
                            id          INTEGER PRIMARY KEY,
                            nombre      VARCHAR({LONG_NOM})
                        )""")

def construir_tabla_recepcionista(cursor: sqlite.Cursor):
    """Construye la tabla Recepcionista"""
    cursor.execute("""CREATE TABLE IF NOT EXISTS Recepcionista (
                            id          INTEGER PRIMARY KEY,
                            dni         INTEGER UNIQUE NOT NULL,
                            FOREIGN KEY (dni) REFERENCES Empleado(dni)
                                        ON UPDATE CASCADE
                                        ON DELETE SET NULL
                        )""")

def construir_tabla_rol(cursor: sqlite.Cursor):
    """Construye la tabla Recepcionista"""
    cursor.execute(f"""CREATE TABLE IF NOT EXISTS Rol (
                            id          INTEGER PRIMARY KEY,
                            nombre      VARCHAR({LONG_NOM})
                        )""")

def construir_tabla_rol_tener_permiso(cursor: sqlite.Cursor):
    """Construye la tabla Permiso"""
    cursor.execute("""CREATE TABLE IF NOT EXISTS Rol_Tener_Permiso (
                            id          INTEGER PRIMARY KEY,
                            rol_id      INTEGER NOT NULL,
                            permiso_id  INTEGER NOT NULL,
                            FOREIGN KEY (rol_id) REFERENCES Rol(id)
                                        ON UPDATE CASCADE
                                        ON DELETE SET NULL,
                            FOREIGN KEY (permiso_id) REFERENCES Permiso(id)
                                        ON UPDATE CASCADE
                                        ON DELETE SET NULL
                        )""")

def construir_tabla_actividad(cursor: sqlite.Cursor):
    """Construye la tabla Actividad"""
    cursor.execute(f"""CREATE TABLE IF NOT EXISTS Actividad (
                            id              INTEGER PRIMARY KEY,
                            nombre          VARCHAR({LONG_NOM}),
                            precio_mensual  REAL
                        )""")

def construir_tabla_profesor(cursor: sqlite.Cursor):
    """Construye la tabla Profesor"""
    cursor.execute(f"""CREATE TABLE IF NOT EXISTS Profesor (
                            id          INTEGER PRIMARY KEY,
                            nombre      VARCHAR({LONG_NOM}),
                            apellido    VARCHAR({LONG_APE}),
                            genero      CHAR(1) CHECK(length(genero) <= 1),
                            dni         INTEGER UNIQUE NOT NULL
                        )""")

def construir_tabla_clase(cursor: sqlite.Cursor):
    """Construye la tabla Clase"""
    cursor.execute(f"""CREATE TABLE IF NOT EXISTS Clase (
                            id           INTEGER PRIMARY KEY,
                            estado       VARCHAR({LONG_NOM}),
                            actividad_id INTEGER NOT NULL,
                            profesor_id  INTEGER NOT NULL,
                            FOREIGN KEY (actividad_id) REFERENCES Actividad(id)
                                        ON UPDATE CASCADE
                                        ON DELETE SET NULL,
                            FOREIGN KEY (profesor_id) REFERENCES Profesor(id)
                                        ON UPDATE CASCADE
                                        ON DELETE SET NULL
                        )""")

def construir_tabla_sala(cursor: sqlite.Cursor):
    """Construye la tabla Sala"""
    cursor.execute(f"""CREATE TABLE IF NOT EXISTS Sala (
                            id          INTEGER PRIMARY KEY,
                            nombre      VARCHAR({LONG_NOM})
                        )""")

def construir_tabla_clase_ocurrir_sala(cursor: sqlite.Cursor):
    """Construye la tabla Clase_Ocurrir_Sala"""
    cursor.execute("""CREATE TABLE IF NOT EXISTS Clase_Ocurrir_Sala (
                            id        INTEGER PRIMARY KEY,
                            clase_id  INTEGER NOT NULL,
                            sala_id   INTEGER NOT NULL,
                            fecha     DATE,
                            FOREIGN KEY (clase_id) REFERENCES Clase(id)
                                        ON UPDATE CASCADE
                                        ON DELETE SET NULL,
                            FOREIGN KEY (sala_id) REFERENCES Sala(id)
                                        ON UPDATE CASCADE
                                        ON DELETE SET NULL
                        )""")

def construir_tabla_usuario(cursor: sqlite.Cursor):
    """Construye la tabla Usuario"""
    cursor.execute(f"""CREATE TABLE IF NOT EXISTS Usuario (
                            id          INTEGER PRIMARY KEY,
                            dni         INTEGER UNIQUE NOT NULL,
                            nombre      VARCHAR({LONG_NOM}),
                            apellido    VARCHAR({LONG_APE}),
                            edad        INTEGER NOT NULL,
                            contraseña  VARCHAR({LONG_CONTRA}),
                            correo      VARCHAR({LONG_CORREO}),
                            telefono    VARCHAR({LONG_TEL}),
                            genero      CHAR(1) CHECK(length(genero) <= 1)
                        )""")

def construir_tabla_descuento(cursor: sqlite.Cursor):
    """Construye la tabla Descuento"""
    cursor.execute(f"""CREATE TABLE IF NOT EXISTS Descuento (
                            id          INTEGER PRIMARY KEY,
                            nombre      VARCHAR({LONG_NOM})
                        )""")

def construir_tabla_usuario_tener_descuento(cursor: sqlite.Cursor):
    """Construye la tabla Usuario_Tener_Descuento"""
    cursor.execute("""CREATE TABLE IF NOT EXISTS Usuario_Tener_Descuento (
                            id           INTEGER PRIMARY KEY,
                            usuario_id   INTEGER NOT NULL,
                            descuento_id INTEGER NOT NULL,
                            FOREIGN KEY (usuario_id) REFERENCES Usuario(id)
                                        ON UPDATE CASCADE
                                        ON DELETE SET NULL,
                            FOREIGN KEY (descuento_id) REFERENCES Descuento(id)
                                        ON UPDATE CASCADE
                                        ON DELETE SET NULL
                        )""")

def construir_tabla_usuario_inscribir_clase(cursor: sqlite.Cursor):
    """Construye la tabla Usuario_Inscribir_Clase"""
    cursor.execute("""CREATE TABLE IF NOT EXISTS Usuario_Inscribir_Clase (
                            id         INTEGER PRIMARY KEY,
                            usuario_id INTEGER NOT NULL,
                            clase_id   INTEGER NOT NULL,
                            fecha      DATE,
                            FOREIGN KEY (usuario_id) REFERENCES Usuario(id)
                                        ON UPDATE CASCADE
                                        ON DELETE SET NULL,
                            FOREIGN KEY (clase_id) REFERENCES Clase(id)
                                        ON UPDATE CASCADE
                                        ON DELETE SET NULL
                        )""")

def construir_tabla_usuario_cancelar_clase(cursor: sqlite.Cursor):
    """Construye la tabla Usuario_Cancelar_Clase"""
    cursor.execute("""CREATE TABLE IF NOT EXISTS Usuario_Cancelar_Clase (
                            id         INTEGER PRIMARY KEY,
                            usuario_id INTEGER NOT NULL,
                            clase_id   INTEGER NOT NULL,
                            FOREIGN KEY (usuario_id) REFERENCES Usuario(id)
                                        ON UPDATE CASCADE
                                        ON DELETE SET NULL,
                            FOREIGN KEY (clase_id) REFERENCES Clase(id)
                                        ON UPDATE CASCADE
                                        ON DELETE SET NULL
                        )""")

def construir_tabla_pago(cursor: sqlite.Cursor):
    """Construye la tabla Pago"""
    cursor.execute("""CREATE TABLE IF NOT EXISTS Pago (
                            id         INTEGER PRIMARY KEY,
                            monto      REAL,
                            usuario_id INTEGER NOT NULL,
                            FOREIGN KEY (usuario_id) REFERENCES Usuario(id)
                                        ON UPDATE CASCADE
                                        ON DELETE SET NULL
                        )""")

def construir_tabla_mensualidad(cursor: sqlite.Cursor):
    """Construye la tabla Mensualidad"""
    cursor.execute("""CREATE TABLE IF NOT EXISTS Mensualidad (
                            id         INTEGER PRIMARY KEY,
                            fecha_ini  DATE,
                            fecha_fin  DATE,
                            usuario_id INTEGER NOT NULL,
                            FOREIGN KEY (usuario_id) REFERENCES Usuario(id)
                                        ON UPDATE CASCADE
                                        ON DELETE SET NULL
                        )""")

def construir_tabla_clase_tener_mensualidad(cursor: sqlite.Cursor):
    """Construye la tabla Clase_Tener_Mensualidad"""
    cursor.execute("""CREATE TABLE IF NOT EXISTS Clase_Tener_Mensualidad (
                            id             INTEGER PRIMARY KEY,
                            mensualidad_id INTEGER NOT NULL,
                            clase_id       INTEGER NOT NULL,
                            FOREIGN KEY (mensualidad_id) REFERENCES Mensualidad(id)
                                        ON UPDATE CASCADE
                                        ON DELETE SET NULL,
                            FOREIGN KEY (clase_id) REFERENCES Clase(id)
                                        ON UPDATE CASCADE
                                        ON DELETE SET NULL
                        )""")

def construir_tabla_pago_pagar_clase(cursor: sqlite.Cursor):
    """Construye la tabla Pago_Pagar_Clase"""
    cursor.execute("""CREATE TABLE IF NOT EXISTS Pago_Pagar_Clase (
                            id       INTEGER PRIMARY KEY,
                            pago_id  INTEGER NOT NULL,
                            clase_id INTEGER NOT NULL,
                            FOREIGN KEY (pago_id) REFERENCES Pago(id)
                                        ON UPDATE CASCADE
                                        ON DELETE SET NULL,
                            FOREIGN KEY (clase_id) REFERENCES Clase(id)
                                        ON UPDATE CASCADE
                                        ON DELETE SET NULL
                        )""")

def construir_tabla_pago_pagar_mensualidad(cursor: sqlite.Cursor):
    """Construye la tabla Pago_Pagar_Mensualidad"""
    cursor.execute("""CREATE TABLE IF NOT EXISTS Pago_Pagar_Mensualidad (
                            id             INTEGER PRIMARY KEY,
                            pago_id        INTEGER NOT NULL,
                            mensualidad_id INTEGER NOT NULL,
                            FOREIGN KEY (pago_id) REFERENCES Pago(id)
                                        ON UPDATE CASCADE
                                        ON DELETE SET NULL,
                            FOREIGN KEY (mensualidad_id) REFERENCES Mensualidad(id)
                                        ON UPDATE CASCADE
                                        ON DELETE SET NULL
                        )""")