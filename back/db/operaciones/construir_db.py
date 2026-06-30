import sqlite3 as sqlite
import os

from db import LONG_TEL, LONG_NOM, LONG_APE, LONG_CORREO, LONG_CONTRA

def reconstruir_db():
    """Destruye la BD y luego la vuelve a construir"""
    ruta_completa = os.path.join(os.getcwd(), os.getenv("NOM_DB"))
    
    try:
        os.remove(ruta_completa)
        print(" > Base de datos anterior eliminada.")
    except FileNotFoundError:
        # Si no existe, no hacemos nada y dejamos que el programa siga
        print(" > La base de datos no existía, saltando la eliminación.")
        
    construir_db()

def construir_db():
    """Construye la BD si no existía antes"""
    conexion = sqlite.connect(os.getenv("NOM_DB"))

    # Y con este podemos ejecutar y obtener resultados de
    # sentencias SQL de la BD
    cursor = conexion.cursor()

    # Habilitar Foreign Keys
    cursor.execute("PRAGMA foreign_keys = ON")

    # Ejecutar funciones que crean las tablas
    construir_tablas(cursor)

    # Prueba de que la BD se creó exitosamente 
    # res = cursor.execute("SELECT name FROM sqlite_master")
    # print(res.fetchall())

    # Cerrar la conexión
    conexion.close()

def construir_tablas(cursor: sqlite.Cursor):
    """Construye todas las tablas de la BD"""
    # Construir tablas para las entidades
    construir_tabla_rol(cursor)
    construir_tabla_actividad(cursor)
    construir_tabla_sala(cursor)
    construir_tabla_descuento(cursor)
    construir_tabla_usuario(cursor)
    construir_tabla_clase(cursor)    # necesita Actividad, Profesor (usuario) y Sala
    construir_tabla_pago(cursor)     # necesita Usuario
    construir_tabla_mensualidad(cursor) # necesita Usuario
    construir_tabla_imagenes(cursor)
    construir_tabla_instancia_clase(cursor)
    construir_tabla_lista_espera_abonados(cursor)   # necesita Clase
    construir_tabla_lista_espera_individual(cursor) # necesita Instancia_Clase
    construir_tabla_asistencias_clase(cursor)       # necesita Usuario e Instancia_Clase

    # Construir tablas para las relaciones
    construir_tabla_usuario_tener_descuento(cursor)
    construir_tabla_profesor_actividad(cursor) 
    construir_tabla_reserva(cursor)
    construir_tabla_cancelacion(cursor)
    construir_tabla_pago_pagar_clase(cursor)
    construir_tabla_pago_pagar_mensualidad(cursor)
    construir_tabla_clase_tener_mensualidad(cursor)
    construir_tabla_usuario_pertenece_lista_espera_abonados(cursor)
    construir_tabla_usuario_pertenece_lista_espera_individual(cursor)
    construir_tabla_profesor_actividad(cursor)
    
    construir_tabla_proximas_notificaciones(cursor)

## FUNCIONES QUE CREAN TABLAS
# En este apartado aparecen todas las funciones que crean
# alguna tabla de la BD.

def construir_tabla_usuario(cursor: sqlite.Cursor):
    """Construye la tabla Usuario"""
    cursor.execute(f"""CREATE TABLE IF NOT EXISTS Usuario (
                            id          INTEGER PRIMARY KEY,
                            dni         INTEGER NOT NULL,
                            nombre      VARCHAR({LONG_NOM}) NOT NULL,
                            apellido    VARCHAR({LONG_APE}) NOT NULL,
                            correo      VARCHAR({LONG_CORREO}),
                            contraseña  VARCHAR({LONG_CONTRA}),
                            fecha_nac   DATE,
                            telefono    VARCHAR({LONG_TEL}),
                            genero      CHAR(1) CHECK(length(genero) <= 1),
                            rol_id      INTEGER NOT NULL,
                            imagen_id   INTEGER,
                            estado      INTEGER NOT NULL DEFAULT 0,
                            FOREIGN KEY (imagen_id) REFERENCES Imagen(id)
                                        ON UPDATE CASCADE
                                        ON DELETE SET NULL
                        )""")

def construir_tabla_imagenes(cursor: sqlite.Cursor):
    """Construye la tabla Imagenes"""
    cursor.execute("""CREATE TABLE IF NOT EXISTS Imagen (
                            id          INTEGER PRIMARY KEY,
                            contenido   BLOB NOT NULL
                        )""")

def construir_tabla_actividad(cursor: sqlite.Cursor):
    """Construye la tabla Actividad"""
    cursor.execute(f"""CREATE TABLE IF NOT EXISTS Actividad (
                            id              INTEGER PRIMARY KEY,
                            nombre          VARCHAR({LONG_NOM}),
                            precio_mensual  REAL NOT NULL
                        )""")

def construir_tabla_clase(cursor: sqlite.Cursor):
    """Construye la tabla Clase"""
    cursor.execute(f"""CREATE TABLE IF NOT EXISTS Clase (
                            id           INTEGER PRIMARY KEY,
                            estado       VARCHAR({LONG_NOM}),
                            actividad_id INTEGER NOT NULL,
                            profesor_id  INTEGER NOT NULL,
                            sala_id      INTEGER NOT NULL,
                            dia          VARCHAR(10) NOT NULL,
                            hora         VARCHAR(5) NOT NULL,
                            cupo_maximo  INTEGER NOT NULL,
                            monto        REAL,
                            FOREIGN KEY  (actividad_id) REFERENCES Actividad(id)
                                         ON UPDATE CASCADE
                                         ON DELETE SET NULL,
                            FOREIGN KEY  (profesor_id) REFERENCES Usuario(id)
                                         ON UPDATE CASCADE
                                         ON DELETE SET NULL,
                            FOREIGN KEY  (sala_id) REFERENCES Sala(id)
                                         ON UPDATE CASCADE
                                         ON DELETE SET NULL
                        )""")

def construir_tabla_sala(cursor: sqlite.Cursor):
    """Construye la tabla Sala"""
    cursor.execute(f"""CREATE TABLE IF NOT EXISTS Sala (
                            id          INTEGER PRIMARY KEY,
                            nombre      VARCHAR({LONG_NOM}),
                            capacidad   INTEGER NOT NULL
                        )""")

def construir_tabla_instancia_clase(cursor: sqlite.Cursor):
    """Construye la tabla Instancia_Clase"""
    cursor.execute("""CREATE TABLE IF NOT EXISTS Instancia_Clase (
                            id        INTEGER PRIMARY KEY,
                            fecha     DATE NOT NULL,
                            clase_id  INTEGER,
                            monto     REAL,
                            FOREIGN KEY (clase_id) REFERENCES Clase(id)
                                        ON UPDATE CASCADE
                                        ON DELETE SET NULL
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

## repensar estas 5 funciones, si necesitan herencia o se diferencian en algo mas

def construir_tabla_reserva(cursor: sqlite.Cursor):
    """Construye la tabla Reserva"""
    cursor.execute("""CREATE TABLE IF NOT EXISTS Reserva (
                            id            INTEGER PRIMARY KEY,
                            usuario_id    INTEGER NOT NULL,
                            inst_clase_id INTEGER NOT NULL,
                            fecha         DATE NOT NULL,
                            FOREIGN KEY (usuario_id) REFERENCES Usuario(id)
                                        ON UPDATE CASCADE
                                        ON DELETE SET NULL,
                            FOREIGN KEY (inst_clase_id) REFERENCES Instancia_Clase(id)
                                        ON UPDATE CASCADE
                                        ON DELETE SET NULL
                        )""")

def construir_tabla_cancelacion(cursor: sqlite.Cursor):
    """Construye la tabla Cancelacion"""
    cursor.execute("""CREATE TABLE IF NOT EXISTS Cancelacion (
                            id            INTEGER PRIMARY KEY,
                            fecha         DATE NOT NULL,
                            usuario_id    INTEGER NOT NULL,
                            inst_clase_id INTEGER NOT NULL,
                            FOREIGN KEY (usuario_id) REFERENCES Usuario(id)
                                        ON UPDATE CASCADE
                                        ON DELETE SET NULL,
                            FOREIGN KEY (inst_clase_id) REFERENCES Instancia_Clase(id)
                                        ON UPDATE CASCADE
                                        ON DELETE SET NULL
                        )""")
    
def construir_tabla_lista_espera_abonados(cursor: sqlite.Cursor):
    """Construye la tabla Lista_Espera_Abonados"""
    cursor.execute("""CREATE TABLE IF NOT EXISTS Lista_Espera_Abonados (
                            id         INTEGER PRIMARY KEY,
                            clase_id   INTEGER,
                            FOREIGN KEY (clase_id) REFERENCES Clase(id)
                                        ON UPDATE CASCADE
                                        ON DELETE SET NULL
                        )""")

def construir_tabla_usuario_pertenece_lista_espera_abonados(cursor: sqlite.Cursor):
    """Construye la tabla Usuario_Pertenece_Lista_Espera_Abonados"""
    cursor.execute("""CREATE TABLE IF NOT EXISTS Usuario_Pertenece_Lista_Espera_Abonados (
                            id            INTEGER PRIMARY KEY,
                            usuario_id    INTEGER NOT NULL,
                            lea_id        INTEGER NOT NULL,
                            fecha         DATE NOT NULL,
                            FOREIGN KEY (usuario_id) REFERENCES Usuario(id)
                                        ON UPDATE CASCADE
                                        ON DELETE SET NULL,
                            FOREIGN KEY (lea_id) REFERENCES Lista_Espera_Abonados(id)
                                        ON UPDATE CASCADE
                                        ON DELETE SET NULL
                        )""")
    
def construir_tabla_lista_espera_individual(cursor: sqlite.Cursor):
    """Construye la tabla Lista_Espera_Individual"""
    cursor.execute("""CREATE TABLE IF NOT EXISTS Lista_Espera_Individual (
                            id         INTEGER PRIMARY KEY,
                            inst_clase_id   INTEGER,
                            FOREIGN KEY (inst_clase_id) REFERENCES Instancia_Clase(id)
                                        ON UPDATE CASCADE
                                        ON DELETE SET NULL
                        )""")

def construir_tabla_usuario_pertenece_lista_espera_individual(cursor: sqlite.Cursor):
    """Construye la tabla Usuario_Pertenece_Lista_Espera_Individual"""
    cursor.execute("""CREATE TABLE IF NOT EXISTS Usuario_Pertenece_Lista_Espera_Individual (
                            id            INTEGER PRIMARY KEY,
                            usuario_id    INTEGER NOT NULL,
                            lei_id        INTEGER NOT NULL,
                            fecha         DATE NOT NULL,
                            FOREIGN KEY (usuario_id) REFERENCES Usuario(id)
                                        ON UPDATE CASCADE
                                        ON DELETE SET NULL,
                            FOREIGN KEY (lei_id) REFERENCES Lista_Espera_Individual(id)
                                        ON UPDATE CASCADE
                                        ON DELETE SET NULL
                        )""")
    
def construir_tabla_asistencias_clase(cursor: sqlite.Cursor):
    """Construye la tabla Asistencias_Clase"""
    cursor.execute("""CREATE TABLE IF NOT EXISTS Asistencias_Clase (
                            id         INTEGER PRIMARY KEY,
                            usuario_id INTEGER NOT NULL,
                            con_mensualidad BOOLEAN NOT NULL,
                            inst_clase_id   INTEGER NOT NULL,
                            FOREIGN KEY (usuario_id) REFERENCES Usuario(id)
                                        ON UPDATE CASCADE
                                        ON DELETE SET NULL,
                            FOREIGN KEY (inst_clase_id) REFERENCES Instancia_Clase(id)
                                        ON UPDATE CASCADE
                                        ON DELETE SET NULL
                        )""")

def construir_tabla_pago(cursor: sqlite.Cursor):
    """Construye la tabla Pago"""
    cursor.execute("""CREATE TABLE IF NOT EXISTS Pago (
                            id         INTEGER PRIMARY KEY,
                            monto      REAL,
                            fecha     DATE,
                            usuario_id INTEGER NOT NULL,
                            estado      VARCHAR(20) NOT NULL,
                            mp_order_id VARCHAR(75) UNIQUE,
                            FOREIGN KEY (usuario_id) REFERENCES Usuario(id)
                                        ON UPDATE CASCADE
                                        ON DELETE SET NULL
                        )""")

# Estado es para saber si una mensualidad esta cancelada con lo cual no se le informa al cliente que se le esta acabando al mail para la renovacion 
# pero sigue teniendo los beneficios de la mensualidad hasta que se le acabe el plazo de la misma
# Estados posibles: 0 -> Activa, 1 -> Cancelada
def construir_tabla_mensualidad(cursor: sqlite.Cursor):
    """Construye la tabla Mensualidad"""
    cursor.execute("""CREATE TABLE IF NOT EXISTS Mensualidad (
                            id         INTEGER PRIMARY KEY,
                            fecha_ini  DATE NOT NULL,
                            fecha_fin  DATE,
                            usuario_id INTEGER NOT NULL,
                            estado BOOLEAN NOT NULL DEFAULT 0, 
                            FOREIGN KEY (usuario_id) REFERENCES Usuario(id)
                                        ON UPDATE CASCADE
                                        ON DELETE SET NULL
                        )""")

def construir_tabla_clase_tener_mensualidad(cursor: sqlite.Cursor):
    """Construye la tabla Clase_Tener_Mensualidad"""
    cursor.execute("""CREATE TABLE IF NOT EXISTS Clase_Tener_Mensualidad (
                            id             INTEGER PRIMARY KEY,
                            mensualidad_id INTEGER NOT NULL,
                            clase_id       INTEGER,
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
                            clase_id INTEGER,
                            FOREIGN KEY (pago_id) REFERENCES Pago(id)
                                        ON UPDATE CASCADE
                                        ON DELETE SET NULL,
                            FOREIGN KEY (clase_id) REFERENCES Instancia_Clase(id)
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

def construir_tabla_rol(cursor: sqlite.Cursor):
    """Construye la tabla Rol"""
    cursor.execute(f"""CREATE TABLE IF NOT EXISTS Rol (
                            id          INTEGER PRIMARY KEY,
                            nombre      VARCHAR({LONG_NOM})
                        )""")

def construir_tabla_profesor_actividad(cursor: sqlite.Cursor):
    """Construye la tabla intermedia Profesor_Actividad"""
    cursor.execute("""CREATE TABLE IF NOT EXISTS Profesor_Actividad (
                            profesor_id  INTEGER NOT NULL,
                            actividad_id INTEGER NOT NULL,
                            PRIMARY KEY (profesor_id, actividad_id),
                            FOREIGN KEY (profesor_id) REFERENCES Usuario(id)
                                         ON UPDATE CASCADE
                                         ON DELETE CASCADE,
                            FOREIGN KEY (actividad_id) REFERENCES Actividad(id)
                                         ON UPDATE CASCADE
                                         ON DELETE CASCADE
                        )""")
    
# tabla para no mandar mas de una notificacion al mismo usuario por la misma mensualidad
# se borran las notificaciones pasadas la semana, 1 vez al mes
def construir_tabla_proximas_notificaciones(cursor: sqlite.Cursor):
    """Construye la tabla Notificaciones_Enviadas"""
    cursor.execute("""CREATE TABLE IF NOT EXISTS Notificaciones_Enviadas (
                            id             INTEGER PRIMARY KEY,
                            mensualidad_id INTEGER NOT NULL UNIQUE,
                            fecha_envio     DATE,
                            FOREIGN KEY (mensualidad_id) REFERENCES Mensualidad(id)
                                        ON UPDATE CASCADE
                                        ON DELETE SET NULL
                        )""")