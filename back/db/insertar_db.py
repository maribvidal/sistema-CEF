import sqlite3 as sqlite;

## CONSTANTES

NOM_DB = "database.db"

## FUNCIÓN QUE CREA LA CONEXIÓN A LA BD Y DEVUELVE UN CURSOR

def conectarse_db() -> sqlite.Cursor:
    conexion = sqlite.connect(NOM_DB);
    cursor = conexion.cursor();
    return cursor;

## FUNCIONES QUE INSERTAN FILAS EN LAS TABLAS DE LA BD

def insertar_fila_permiso(nombre):
    cursor = conectarse_db();
    cursor.execute(f"""INSERT INTO Permiso (nombre)
                             VALUES ('{nombre}');""");
    cursor.connection.commit();
    cursor.connection.close();

# insertar_fila_permiso('Modificar');