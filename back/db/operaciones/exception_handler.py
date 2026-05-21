import sqlite3 as sqlite

def ejecutar_fetchall(cursor, query):
    """Ejecuta una consulta SQL que devuelve varias filas y 
        maneja las excepciones."""
    try:
        cursor.execute(query)
        resultado = cursor.fetchall()

        # me tiraba error por el tipo de dato que devuelve el fetchall, así que lo convertí a una lista de diccionarios
        datos = [dict(fila) for fila in resultado]

        return {
            "status": "success",
            "data": datos
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }


def ejecutar_fetchone(cursor, query):
    """Ejecuta una consulta SQL que devuelve una sola fila y
        maneja las excepciones."""
    try:
        cursor.execute(query)
        resultado = cursor.fetchone()

        return {
            "status": "success",
            "data": resultado
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
        
def ejecutar_insertar(cursor, query) -> int:
    """Ejecuta una consulta SQL de inserción y maneja 
        las excepciones."""
    try:
        cursor.execute(query)
        nuevo_id = cursor.lastrowid
        cursor.connection.commit()
        return nuevo_id
    except sqlite.IntegrityError as e:
        print(f" > Error de integridad al ejecutar inserción: {e}")
        return -1
    except Exception as e:
        print(f" > Error al ejecutar inserción: {e}")
        return -1

def ejecutar_query(cursor, query) -> tuple:
    """Ejecuta una consulta SQL que no devuelve datos 
        y maneja las excepciones."""
    try:
        cursor.execute(query)
        cursor.connection.commit()
        return True
    except Exception as e:
        print(f" > Error al ejecutar consulta: {e}")
        return False