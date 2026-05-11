alumnos@biblioteca-alumnos02:~$ cat ins.py
import sqlite3 as sqlite;

## CONSTANTES

NOM_DB = "database.db"

## FUNCIÓN QUE CREA LA CONEXIÓN A LA BD Y DEVUELVE UN CURSOR

def conectarse_db() -> sqlite.Cursor:
    conexion = sqlite.connect(NOM_DB);
    cursor = conexion.cursor();
    return cursor;

## FUNCIONES QUE INSERTAN FILAS EN LAS TABLAS DE LA BD

def insertar_permiso(nombre):
    cursor = conectarse_db();
    cursor.execute(f"""INSERT INTO Permiso (nombre)
                             VALUES ('{nombre}');""");
    cursor.connection.commit();
    cursor.connection.close();

def insertar_rol(nombre):
    cursor = conectarse_db();
    cursor.execute(f"INSERT INTO Rol (nombre) VALUES ('{nombre}')");

    cursor.connection.commit();
    cursor.connection.close();

# - ¿Descuento y Sala deberían tener otro atributo?

def insertar_profesor(nombre, apellido, genero, dni):
    cursor = conectarse_db();
    cursor.ex

    cursor.connection.commit();
    cursor.connection.close();

# insertar_permiso('Modificar');
