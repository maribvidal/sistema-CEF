import sqlite3 as sqlite;

## CONSTANTES

NOM_DB = "database.db"

## FUNCIONES DE CONEXIÓN CON LA BD

def conectarse_db() -> sqlite.Cursor:
    conexion = sqlite.connect(NOM_DB);
    cursor = conexion.cursor();
    return cursor;

def commitear(cursor: sqlite.Cursor):
    cursor.connection.commit();
    cursor.connection.close();

## FUNCIONES QUE INSERTAN FILAS EN LAS TABLAS DE LA BD

def insertar_permiso(nombre):
    cursor = conectarse_db();
    cursor.execute(f"""INSERT INTO Permiso (nombre)
                                VALUES ('{nombre}');""");
    commitear(cursor);

def insertar_rol(nombre):
    cursor = conectarse_db();
    cursor.execute(f"""INSERT INTO Rol (nombre) 
                                VALUES ('{nombre}')""");
    commitear(cursor);

def insertar_profesor(nombre, apellido, genero, dni):
    cursor = conectarse_db();
    cursor.execute(f"""INSERT INTO Profesor (nombre, apellido, genero, dni)
                                VALUES('{nombre}', '{apellido}', '{genero}', '{dni}')""");
    commitear(cursor);

# insertar_permiso('Modificar');